from bson import ObjectId
from beanie import Document

from .. import models, schemas
from .base_repo import BaseRepository
from api_app.api.core.exceptions import ValidationError

from loguru import logger
from ..utils.schema import PydanticObjectId
from fastapi_pagination.ext.beanie import paginate as beanie_paginate
from fastapi_pagination import Page, Params


class UserTicketRepository(BaseRepository):
    def __init__(self):
        super().__init__(models.UserTicket)

    async def get_user_ticket_by_id(
        self, user_ticket_id: str, fetch_links: bool
    ) -> Document:
        if not ObjectId.is_valid(user_ticket_id):
            raise ValidationError("Invalid ObjectId")

        item = await self.model.get(
            PydanticObjectId(user_ticket_id), fetch_links=fetch_links
        )
        if not item:
            raise ValidationError(f"ObjectId('{user_ticket_id}') not found")
        return item

    async def get_user_tickets(self) -> list[Document]:
        items = await self.model.find().to_list()
        return items

    async def get_tickets_by_user_id(self, user_id: str) -> list[Document]:
        if not ObjectId.is_valid(user_id):
            raise ValidationError("Invalid ObjectId")

        items = await self.model.find({"user": PydanticObjectId(user_id)}).to_list()
        if not items:
            raise ValidationError(f"ObjectId('{user_id}') not found")
        return items
