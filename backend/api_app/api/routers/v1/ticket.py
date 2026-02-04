"""Ticket booking endpoints with race condition prevention."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

from api_app import models
from api_app.services.ticket_booking_service import TicketBookingService
from api_app.api.core import dependencies
from api_app.api.core.redis import get_redis
from redis.asyncio import Redis


router = APIRouter(prefix="/tickets", tags=["tickets"])


class TicketBookingRequest(BaseModel):
    event_id: str = Field(..., description="Event ID")
    ticket_type_id: str = Field(..., description="Ticket type ID")
    quantity: int = Field(
        ..., gt=0, le=10, description="Number of tickets (max 10 per booking)"
    )


class TicketCancellationRequest(BaseModel):
    event_id: str = Field(..., description="Event ID")
    ticket_type_id: str = Field(..., description="Ticket type ID")
    quantity: int = Field(..., gt=0, description="Number of tickets to cancel")


@router.post("/book")
async def book_tickets(
    booking: TicketBookingRequest,
    current_user: models.User = Depends(dependencies.get_current_user),
    redis: Redis = Depends(get_redis),
):
    service = TicketBookingService(redis)
    result = await service.book_tickets(
        event_id=booking.event_id,
        ticket_type_id=booking.ticket_type_id,
        quantity=booking.quantity,
        user_id=str(current_user.id),
    )

    return result


@router.get("/{event_id}/inventory")
async def get_event_inventory(event_id: str, redis: Redis = Depends(get_redis)):
    """
    Get full inventory status for all ticket types of an event.
    """
    from api_app.repositories import EventRepository

    repo = EventRepository()
    event = await repo.get_event_by_id(event_id)

    if not event:
        raise HTTPException(404, "Event not found")

    service = TicketBookingService(redis)
    inventory_status = []

    for ticket_type in event.ticket_types:
        availability = await service.get_ticket_availability(
            event_id, ticket_type.ticket_id
        )

        redis_key = f"inventory:event:{event_id}:ticket:{ticket_type.ticket_id}"
        redis_value = await redis.get(redis_key)

        inventory_status.append(
            {
                "ticket_type_id": ticket_type.ticket_id,
                "ticket_name": ticket_type.name,
                "price": ticket_type.price,
                "total": ticket_type.total,
                "available_redis": availability["available"] if availability else None,
                "remaining_db": ticket_type.remaining,
                "redis_key": redis_key,
                "redis_raw_value": redis_value,
                "redis_value_type": str(type(redis_value)),
            }
        )

    return {
        "event_id": event_id,
        "event_name": event.name,
        "inventory": inventory_status,
    }


@router.get("/debug/redis/{event_id}")
async def debug_redis_inventory(event_id: str, redis: Redis = Depends(get_redis)):
    """
    Debug endpoint to check Redis inventory directly.
    Shows raw Redis values and types to diagnose inventory issues.
    """
    from api_app.repositories import EventRepository

    repo = EventRepository()
    event = await repo.get_event_by_id(event_id)

    if not event:
        raise HTTPException(404, "Event not found")

    service = TicketBookingService(redis)
    debug_info = []

    for ticket_type in event.ticket_types:
        redis_key = f"inventory:event:{event_id}:ticket:{ticket_type.ticket_id}"

        raw_value = await redis.get(redis_key)

        try:
            class_value = await service.inventory.get_available_tickets(
                event_id, ticket_type.ticket_id
            )
        except Exception as e:
            class_value = f"Error: {str(e)}"

        exists = await redis.exists(redis_key)

        debug_info.append(
            {
                "ticket_type_id": ticket_type.ticket_id,
                "ticket_name": ticket_type.name,
                "redis_key": redis_key,
                "redis_exists": bool(exists),
                "raw_value": raw_value,
                "raw_value_type": str(type(raw_value)),
                "raw_value_length": len(str(raw_value)) if raw_value else 0,
                "class_value": class_value,
                "db_total": ticket_type.total,
                "db_remaining": ticket_type.remaining,
                "db_booked": ticket_type.total - ticket_type.remaining,
            }
        )

    return {
        "event_id": event_id,
        "event_name": event.name,
        "debug_info": debug_info,
        "redis_connection": str(redis),
        "redis_decode_responses": getattr(
            redis.connection_pool.connection_kwargs, "decode_responses", "unknown"
        ),
    }
