from bson import ObjectId
from beanie import Document

from .. import models, schemas
from .base_repo import BaseRepository
from api_app.api.core.exceptions import ValidationError

from loguru import logger
from ..utils.schema import PydanticObjectId
from fastapi_pagination.ext.beanie import paginate as beanie_paginate
from fastapi_pagination import Page, Params


class EventRepository(BaseRepository):
    def __init__(self):
        super().__init__(models.Event)

    async def get_event_by_id(self, event_id: str) -> Document:
        if not ObjectId.is_valid(event_id):
            raise ValidationError("Invalid ObjectId")

        item = await self.model.get(PydanticObjectId(event_id))
        if not item:
            raise ValidationError(f"ObjectId('{event_id}') not found")
        return item
