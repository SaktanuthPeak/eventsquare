import typing as t
from fastapi import APIRouter, Depends, HTTPException, Request, status
from redis.asyncio import Redis

from api_app import schemas, models
from api_app.services import EventService
from ...core import dependencies
from ...core.redis import get_redis
from beanie.operators import Set
from beanie import PydanticObjectId
import datetime
from loguru import logger
from fastapi_pagination import Page, paginate, Params


router = APIRouter(prefix="/events", tags=["events"])


@router.post("")
async def create_event(
    event_create: schemas.EventCreate,
    current_user: models.User = Depends(dependencies.get_current_user),
    service: EventService = Depends(EventService),
    redis: Redis = Depends(get_redis),
) -> schemas.EventResponse:
    event = await service.create_event(event_create, redis=redis)
    return event


@router.get("/{event_id}")
async def get_event_by_id(
    event_id: str,
    current_user: models.User = Depends(dependencies.get_current_user),
    service: EventService = Depends(EventService),
) -> schemas.EventResponse:
    event = await service.get_event_by_id(event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )
    return event


@router.get("")
async def get_events(
    params: Params = Depends(),
    search_params: schemas.EventSearch = Depends(),
    service: EventService = Depends(EventService),
) -> Page[schemas.EventResponse]:
    events = await service.get_events(params, search_params=search_params)

    return events


@router.put("/{event_id}")
async def update_event(
    event_id: str,
    event_update: schemas.EventUpdate,
    current_user: models.User = Depends(dependencies.get_current_user),
    service: EventService = Depends(EventService),
    redis: Redis = Depends(get_redis),
) -> schemas.EventResponse:
    event = await service.update_event(event_id, event_update, redis=redis)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )
    return event


@router.delete("/{event_id}")
async def delete_event(
    event_id: str,
    current_user: models.User = Depends(dependencies.get_current_user),
    service: EventService = Depends(EventService),
    redis: Redis = Depends(get_redis),
) -> dict:
    result = await service.delete_event(event_id, redis=redis)
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )
    return result
