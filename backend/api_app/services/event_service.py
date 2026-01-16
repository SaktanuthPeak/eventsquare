from fastapi import (
    Request,
)

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
    ) -> schemas.EventResponse:
        event = await self._repository.create(event_create)
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
