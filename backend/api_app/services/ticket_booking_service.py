"""Ticket booking service with race condition prevention."""

from typing import Optional
from fastapi import HTTPException
from redis.asyncio import Redis
from loguru import logger

from .. import models, schemas
from ..repositories import EventRepository
from ..services import BaseService
from ..api.core.redis_lock import TicketInventory, RedisLock
from datetime import datetime


class TicketBookingService(BaseService):
    def __init__(self, redis: Redis):
        event_repository = EventRepository()
        super().__init__(event_repository)
        self.redis = redis
        self.inventory = TicketInventory(redis)

    async def book_tickets(
        self,
        booking: schemas.TicketBooking,
        user: models.User,
    ) -> dict:
        # Reserve tickets in Redis (with lock)
        reservation_result = await self.inventory.reserve_tickets(
            event_id=booking.event_id,
            ticket_type_id=booking.ticket_type_id,
            quantity=booking.quantity,
            user_id=user.id,
        )

        if not reservation_result["success"]:
            raise HTTPException(
                400, detail=reservation_result.get("error", "Booking failed")
            )

        try:
            event = await self._repository.get_event_by_id(booking.event_id)

            if not event:
                await self.inventory.release_tickets(
                    booking.event_id,
                    booking.ticket_type_id,
                    booking.quantity,
                    "event_not_found",
                )
                raise HTTPException(404, "Event not found")

            # Find and update ticket type
            ticket_type_updated = False
            for ticket_type in event.ticket_types:
                if ticket_type.ticket_id == booking.ticket_type_id:
                    ticket_type.remaining -= booking.quantity
                    ticket_type_updated = True
                    break

            if not ticket_type_updated:
                # Release tickets back to Redis
                await self.inventory.release_tickets(
                    booking.event_id,
                    booking.ticket_type_id,
                    booking.quantity,
                    "ticket_type_not_found",
                )
                raise HTTPException(404, "Ticket type not found")

            # Save to database
            await event.save()

            logger.info(
                f"Booking successful: event={booking.event_id}, ticket={booking.ticket_type_id}, "
                f"quantity={booking.quantity}, user={user.id}, remaining={reservation_result['remaining']}"
            )

            user_ticket = models.UserTicket(
                user=user,
                event=event,
                ticket_name=booking.ticket_type_name,
                ticket_type_id=booking.ticket_type_id,
                price_per_ticket=booking.price_per_ticket,
                total_price=booking.total_price,
                quantity=booking.quantity,
                status="booked",
                event_start_date=event.start_date,
                event_end_date=event.end_date,
                is_checked_in=False,
                checked_in_date=None,
            )
            await user_ticket.insert()

            return {
                "success": True,
                "message": "Booking successful",
                "booking_details": {
                    "event_id": booking.event_id,
                    "ticket_type_id": booking.ticket_type_id,
                    "quantity": booking.quantity,
                    "remaining_tickets": reservation_result["remaining"],
                },
            }

        except Exception as e:
            logger.error(f"Booking failed, rolling back: {str(e)}")
            await self.inventory.release_tickets(
                booking.event_id,
                booking.ticket_type_id,
                booking.quantity,
                "booking_failed",
            )
            raise

    async def sync_inventory_from_db(self, event_id: str) -> dict:
        """
        Sync Redis inventory from database.
        Use this when Redis data is lost or inconsistent.

        Args:
            event_id: Event ID

        Returns:
            Sync result with before/after values
        """
        event = await self._repository.get_event_by_id(event_id)

        if not event:
            raise HTTPException(404, "Event not found")

        synced_tickets = []

        for ticket_type in event.ticket_types:
            redis_key = f"inventory:event:{event_id}:ticket:{ticket_type.ticket_id}"

            # Get old value
            old_value = await self.redis.get(redis_key)

            # Sync from database
            await self.inventory.sync_from_database(
                event_id=str(event.id),
                ticket_type_id=ticket_type.ticket_id,
                remaining_tickets=ticket_type.remaining,
            )

            # Get new value
            new_value = await self.redis.get(redis_key)

            synced_tickets.append(
                {
                    "ticket_type_id": ticket_type.ticket_id,
                    "ticket_name": ticket_type.name,
                    "old_redis_value": old_value,
                    "new_redis_value": new_value,
                    "db_remaining": ticket_type.remaining,
                    "synced": new_value == str(ticket_type.remaining),
                }
            )

        logger.info(f"Synced inventory from DB for event: {event_id}")

        return {
            "success": True,
            "event_id": event_id,
            "event_name": event.name,
            "synced_tickets": synced_tickets,
        }

    async def check_inventory_sync(self, event_id: str) -> dict:
        """
        Check if Redis inventory is in sync with database.

        Args:
            event_id: Event ID

        Returns:
            Comparison between Redis and DB values
        """
        event = await self._repository.get_event_by_id(event_id)

        if not event:
            raise HTTPException(404, "Event not found")

        comparison = []
        has_mismatch = False

        for ticket_type in event.ticket_types:
            redis_key = f"inventory:event:{event_id}:ticket:{ticket_type.ticket_id}"
            redis_value = await self.redis.get(redis_key)
            redis_remaining = int(redis_value) if redis_value else None
            db_remaining = ticket_type.remaining

            is_synced = redis_remaining == db_remaining
            if not is_synced:
                has_mismatch = True

            comparison.append(
                {
                    "ticket_type_id": ticket_type.ticket_id,
                    "ticket_name": ticket_type.name,
                    "redis_remaining": redis_remaining,
                    "db_remaining": db_remaining,
                    "difference": (redis_remaining or 0) - db_remaining,
                    "is_synced": is_synced,
                }
            )

        return {
            "event_id": event_id,
            "event_name": event.name,
            "is_synced": not has_mismatch,
            "comparison": comparison,
            "message": (
                "In sync"
                if not has_mismatch
                else "Out of sync - use /sync endpoint to fix"
            ),
        }
