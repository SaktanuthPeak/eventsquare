from fastapi import (
    Request,
)
from redis.asyncio import Redis
from typing import Optional
from loguru import logger

from ..repositories import UserTicketRepository

from .. import models, schemas
from ..services import BaseService
from fastapi_pagination import Page, Params, paginate
from fastapi_pagination.ext.beanie import paginate as beanie_paginate
import datetime


class UserTicketService(BaseService):
    def __init__(self):
        user_ticket_repository = UserTicketRepository()
        super().__init__(user_ticket_repository)

    async def get_user_ticket_by_id(
        self,
        user_ticket_id: str,
    ) -> schemas.UserTicketDetailResponse:
        user_ticket = await self._repository.get_user_ticket_by_id(
            user_ticket_id, fetch_links=True
        )
        return user_ticket
