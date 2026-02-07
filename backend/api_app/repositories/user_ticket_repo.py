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
        self, user_ticket_id: str, fetch_links: bool = False
    ) -> Document:
        if not ObjectId.is_valid(user_ticket_id):
            raise ValidationError("Invalid ObjectId")

        item = await self.model.get(
            PydanticObjectId(user_ticket_id), fetch_links=fetch_links
        )
        if not item:
            raise ValidationError(f"ObjectId('{user_ticket_id}') not found")
        return item

    async def get_user_tickets(
        self, user_id: str = None, fetch_links: bool = False
    ) -> list[Document]:
        if user_id and not ObjectId.is_valid(user_id):
            raise ValidationError("Invalid ObjectId")
        if user_id:
            items = await self.model.find(
                {self.model.user.id: PydanticObjectId(user_id)},
                fetch_links=fetch_links,
            ).to_list()
        else:
            items = await self.model.find(fetch_links=fetch_links).to_list()
        return items

    async def get_checked_in_users_query(
        self,
        event_id: str,
    ) -> list[Document]:
        if not ObjectId.is_valid(event_id):
            raise ValidationError("Invalid ObjectId")

        query = models.UserTicket.find(
            {
                (self.model.event.id): PydanticObjectId(event_id),
                "is_checked_in": True,
            },
            fetch_links=True,
        )
        return query
