from bson import ObjectId
from beanie import Document

from .. import models, schemas
from .base_repo import BaseRepository
from api_app.api.core.exceptions import ValidationError

from loguru import logger
from ..utils.schema import PydanticObjectId
from fastapi_pagination.ext.beanie import paginate as beanie_paginate
from fastapi_pagination import Page, Params


class TicketRepository(BaseRepository):
    def __init__(self):
        super().__init__(models.Ticket)

    async def get_ticket_by_id(self, ticket_id: str) -> Document:
        if not ObjectId.is_valid(ticket_id):
            raise ValidationError("Invalid ObjectId")

        item = await self.model.get(PydanticObjectId(ticket_id))
        if not item:
            raise ValidationError(f"ObjectId('{ticket_id}') not found")
        return item
