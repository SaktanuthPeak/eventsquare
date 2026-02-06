from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

from api_app import models, schemas
from api_app.services.ticket_booking_service import TicketBookingService
from api_app.api.core import dependencies
from api_app.api.core.redis import get_redis
from redis.asyncio import Redis
from api_app.api.utils.google import pubsub_client
from datetime import datetime
from bson import ObjectId

from api_app import models
from api_app.api.core.redis import get_redis

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.post("/book")
async def book_tickets(
    booking: schemas.TicketBooking,
    current_user: models.User = Depends(dependencies.get_current_user),
    redis: Redis = Depends(get_redis),
):
    service = TicketBookingService(redis)
    result = await service.book_tickets(
        booking=booking,
        user=current_user,
    )

    booking_details = result.get("booking_details", {})

    payload = {
        "event_name": booking_details.get("event_name", ""),
        "event_id": booking.event_id,
        "ticket_id": booking_details.get("ticket_id", ""),
        "ticket_type_name": booking.ticket_type_name,
        "quantity": booking.quantity,
        "total_price": booking.total_price,
        "price_per_ticket": booking.price_per_ticket,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "email": current_user.email,
    }
    try:
        msg_id = pubsub_client.publish_message(
            topic_name="ticket-bookings",
            data=payload,
        )
    except Exception as e:
        print(f"Failed to publish message to Pub/Sub: {str(e)}")
    return result


@router.post("/sync/{event_id}")
async def sync_inventory(
    event_id: str,
    redis: Redis = Depends(get_redis),
):
    """
    Sync Redis inventory from database.

    Use this when Redis data is inconsistent with database.
    This will overwrite Redis with database values.
    """
    service = TicketBookingService(redis)
    return await service.sync_inventory_from_db(event_id)


@router.get("/check-sync/{event_id}")
async def check_sync_status(
    event_id: str,
    redis: Redis = Depends(get_redis),
):
    """
    Check if Redis inventory is in sync with database.

    Returns comparison between Redis and DB values.
    """
    service = TicketBookingService(redis)
    return await service.check_inventory_sync(event_id)


@router.post("/check-in/{ticket_id}")
async def check_in_ticket(
    ticket_id: str,
    # current_user: models.User = Depends(dependencies.get_current_user),
):
    """
    Check-in ticket by QR scan
    """

    try:
        ticket = await models.UserTicket.find_one(
            models.UserTicket.id == ObjectId(ticket_id), fetch_links=True
        )

        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")

        # ยกเลิก / คืนเงิน / หมดอายุ
        if ticket.status != "booked":
            raise HTTPException(
                status_code=400, detail=f"Ticket status = {ticket.status}"
            )

        # สแกนซ้ำ
        if ticket.is_checked_in:
            return {
                "status": "already_used",
                "message": "Ticket already checked in",
                "checked_in_at": ticket.checked_in_date,
            }

        now = datetime.now()

        # อัพเดท ticket
        ticket.is_checked_in = True
        ticket.checked_in_date = now
        await ticket.save()

        return {
            "status": "success",
            "message": "Check-in successful",
            "ticket_id": str(ticket.id),
            "ticket_name": ticket.ticket_name,
            "event_name": ticket.event.name if ticket.event else "Unknown Event",
            "checked_in_at": now,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
