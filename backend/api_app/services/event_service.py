from fastapi import (
    Request,
)
from redis.asyncio import Redis
from typing import Optional
from loguru import logger

from ..repositories import EventRepository

from .. import models, schemas
from ..services import BaseService
from fastapi_pagination import Page, Params, paginate
from fastapi_pagination.ext.beanie import paginate as beanie_paginate
import datetime


class EventService(BaseService):
    def __init__(self):
        event_repository = EventRepository()
        super().__init__(event_repository)

    async def get_event_by_id(
        self,
        event_id: str,
    ) -> schemas.EventResponse:
        event = await self._repository.get_event_by_id(event_id)
        return event

    async def create_event(
        self,
        event_create: schemas.EventCreate,
        redis: Optional[Redis] = None,
    ) -> schemas.EventResponse:
        event = await self._repository.create(event_create)

        if redis:
            from ..api.core.redis_lock import TicketInventory

            inventory = TicketInventory(redis)

            for ticket_type in event.ticket_types:
                try:
                    await inventory.initialize_inventory(
                        event_id=str(event.id),
                        ticket_type_id=ticket_type.ticket_id,
                        total_tickets=ticket_type.remaining,
                    )
                    logger.info(
                        f"Initialized inventory: event={event.id}, "
                        f"ticket={ticket_type.ticket_id}, total={ticket_type.remaining}"
                    )
                except Exception as e:
                    logger.error(f"Failed to initialize inventory: {str(e)}")

        return event

    async def get_events(
        self,
        params: Params,
        search_params: schemas.EventSearch | None = None,
    ) -> Page[schemas.EventResponse]:

        query = {}
        if search_params:
            if search_params.name:
                query["name"] = {
                    "$regex": search_params.name,
                    "$options": "i",
                }
            if search_params.event_type:
                query["event_type"] = search_params.event_type

            if search_params.start_date_from or search_params.start_date_to:
                date_conditions = {}
                if search_params.start_date_from:
                    date_from = datetime.datetime.strptime(
                        search_params.start_date_from, "%Y-%m-%d"
                    )
                    date_conditions["$gte"] = date_from
                if search_params.start_date_to:
                    date_to = datetime.datetime.strptime(
                        search_params.start_date_to, "%Y-%m-%d"
                    )
                    date_to = date_to.replace(
                        hour=23, minute=59, second=59, microsecond=999999
                    )
                    date_conditions["$lte"] = date_to
                if date_conditions:
                    query["start_date"] = date_conditions

        query = models.Event.find(query)
        return await beanie_paginate(query, params)

    async def update_event(
        self,
        event_id: str,
        event_update: schemas.EventUpdate,
        redis: Optional[Redis] = None,
    ) -> schemas.EventResponse:
        if event_update.ticket_types is not None:
            import uuid

            processed_ticket_types = []
            for ticket in event_update.ticket_types:
                if hasattr(ticket, "ticket_id") and ticket.ticket_id:
                    processed_ticket_types.append(ticket)
                else:
                    ticket_db = schemas.TicketTypeDB(
                        name=ticket.name,
                        total=ticket.total,
                        price=ticket.price,
                        remaining=ticket.remaining,
                        ticket_id=str(uuid.uuid4()),
                    )
                    processed_ticket_types.append(ticket_db)

            event_update.ticket_types = processed_ticket_types

        event = await self._repository.update(event_id, event_update)

        if redis and event_update.ticket_types is not None:
            from ..api.core.redis_lock import TicketInventory

            inventory = TicketInventory(redis)

            for ticket_type in event.ticket_types:
                try:
                    # Sync from database to ensure Redis matches the updated values
                    await inventory.sync_from_database(
                        event_id=str(event.id),
                        ticket_type_id=ticket_type.ticket_id,
                        remaining_tickets=ticket_type.remaining,
                    )
                    logger.info(
                        f"Synced inventory after update: event={event.id}, "
                        f"ticket={ticket_type.ticket_id}, remaining={ticket_type.remaining}"
                    )
                except Exception as e:
                    logger.error(f"Failed to sync inventory after update: {str(e)}")

        return event

    async def delete_event(
        self,
        event_id: str,
    ) -> None:
        await self._repository.delete_by_id(event_id)
