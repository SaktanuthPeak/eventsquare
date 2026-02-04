"""Ticket booking endpoints with race condition prevention."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

from api_app import models, schemas
from api_app.services.ticket_booking_service import TicketBookingService
from api_app.api.core import dependencies
from api_app.api.core.redis import get_redis
from redis.asyncio import Redis


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
