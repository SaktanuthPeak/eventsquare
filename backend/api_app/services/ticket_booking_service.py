"""Ticket booking service with race condition prevention."""

from typing import Optional
from fastapi import HTTPException
from redis.asyncio import Redis
from loguru import logger

from .. import models, schemas
from ..repositories import EventRepository
from ..services import BaseService
from ..api.core.redis_lock import TicketInventory, RedisLock


class TicketBookingService(BaseService):
    """Service for handling ticket bookings with Redis-based race condition prevention."""

    def __init__(self, redis: Redis):
        event_repository = EventRepository()
        super().__init__(event_repository)
        self.redis = redis
        self.inventory = TicketInventory(redis)

    async def initialize_event_inventory(self, event_id: str) -> bool:
        """
        Initialize ticket inventory in Redis when event is created.

        Args:
            event_id: Event ID

        Returns:
            True if initialized successfully
        """
        # Get event from database
        event = await self._repository.get_event_by_id(event_id)

        if not event:
            raise HTTPException(404, "Event not found")

        # Initialize inventory for each ticket type
        for ticket_type in event.ticket_types:
            await self.inventory.initialize_inventory(
                event_id=str(event.id),
                ticket_type_id=ticket_type.ticket_id,
                total_tickets=ticket_type.remaining,
            )
            logger.info(
                f"Initialized inventory: event={event_id}, "
                f"ticket={ticket_type.ticket_id}, total={ticket_type.remaining}"
            )

        return True

    async def get_ticket_availability(self, event_id: str, ticket_type_id: str) -> dict:
        """
        Get real-time ticket availability from Redis.

        Args:
            event_id: Event ID
            ticket_type_id: Ticket type ID

        Returns:
            dict with availability info
        """
        available = await self.inventory.get_available_tickets(event_id, ticket_type_id)

        if available is None:
            # Try to sync from database
            event = await self._repository.get_event_by_id(event_id)
            if not event:
                raise HTTPException(404, "Event not found")

            # Find ticket type
            ticket_type = next(
                (tt for tt in event.ticket_types if tt.ticket_id == ticket_type_id),
                None,
            )

            if not ticket_type:
                raise HTTPException(404, "Ticket type not found")

            # Initialize from database
            await self.inventory.initialize_inventory(
                event_id, ticket_type_id, ticket_type.remaining
            )
            available = ticket_type.remaining

        return {
            "event_id": event_id,
            "ticket_type_id": ticket_type_id,
            "available": available,
        }

    async def book_tickets(
        self, event_id: str, ticket_type_id: str, quantity: int, user_id: str
    ) -> dict:
        """
        Book tickets with race condition prevention.

        This method:
        1. Uses distributed lock to prevent race conditions
        2. Reserves tickets in Redis atomically
        3. Updates database
        4. Returns booking confirmation

        Args:
            event_id: Event ID
            ticket_type_id: Ticket type ID
            quantity: Number of tickets to book
            user_id: User ID

        Returns:
            Booking result
        """
        # Reserve tickets in Redis (with lock)
        reservation_result = await self.inventory.reserve_tickets(
            event_id=event_id,
            ticket_type_id=ticket_type_id,
            quantity=quantity,
            user_id=user_id,
        )

        if not reservation_result["success"]:
            raise HTTPException(
                400, detail=reservation_result.get("error", "Booking failed")
            )

        try:
            # Update database
            event = await self._repository.get_event_by_id(event_id)

            if not event:
                # Release tickets back to Redis
                await self.inventory.release_tickets(
                    event_id, ticket_type_id, quantity, "event_not_found"
                )
                raise HTTPException(404, "Event not found")

            # Find and update ticket type
            ticket_type_updated = False
            for ticket_type in event.ticket_types:
                if ticket_type.ticket_id == ticket_type_id:
                    ticket_type.remaining -= quantity
                    ticket_type_updated = True
                    break

            if not ticket_type_updated:
                # Release tickets back to Redis
                await self.inventory.release_tickets(
                    event_id, ticket_type_id, quantity, "ticket_type_not_found"
                )
                raise HTTPException(404, "Ticket type not found")

            # Save to database
            await event.save()

            logger.info(
                f"Booking successful: event={event_id}, ticket={ticket_type_id}, "
                f"quantity={quantity}, user={user_id}, remaining={reservation_result['remaining']}"
            )

            return {
                "success": True,
                "message": "Booking successful",
                "booking_details": {
                    "event_id": event_id,
                    "ticket_type_id": ticket_type_id,
                    "quantity": quantity,
                    "user_id": user_id,
                    "remaining_tickets": reservation_result["remaining"],
                },
            }

        except Exception as e:
            # Rollback: Release tickets back to Redis
            logger.error(f"Booking failed, rolling back: {str(e)}")
            await self.inventory.release_tickets(
                event_id, ticket_type_id, quantity, "booking_failed"
            )
            raise

    async def sync_inventory_from_db(self, event_id: str) -> dict:
        """
        Sync Redis inventory from database.
        Use this if Redis data is lost or inconsistent.

        Args:
            event_id: Event ID

        Returns:
            Sync result
        """
        event = await self._repository.get_event_by_id(event_id)

        if not event:
            raise HTTPException(404, "Event not found")

        synced_tickets = []

        for ticket_type in event.ticket_types:
            await self.inventory.sync_from_database(
                event_id=str(event.id),
                ticket_type_id=ticket_type.ticket_id,
                remaining_tickets=ticket_type.remaining,
            )
            synced_tickets.append(
                {
                    "ticket_type_id": ticket_type.ticket_id,
                    "ticket_name": ticket_type.name,
                    "remaining": ticket_type.remaining,
                }
            )

        logger.info(f"Synced inventory from DB for event: {event_id}")

        return {"success": True, "event_id": event_id, "synced_tickets": synced_tickets}
