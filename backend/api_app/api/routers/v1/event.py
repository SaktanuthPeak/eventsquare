import typing as t
from fastapi import APIRouter, Depends, HTTPException, Request, status
from api_app import schemas, models
from api_app.services import EventService
from ...core import dependencies
from beanie.operators import Set
from beanie import PydanticObjectId
import datetime
from loguru import logger


router = APIRouter(prefix="/events", tags=["events"])


@router.post("")
async def create_event(
    event_create: schemas.EventCreate,
    current_user: models.User = Depends(dependencies.get_current_user),
    service: EventService = Depends(EventService),
) -> schemas.EventResponse:
    event = await service.create(event_create)
    return event
