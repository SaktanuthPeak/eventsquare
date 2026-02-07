from fastapi import (
    Request,
)
from redis.asyncio import Redis
from typing import Optional, List
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

    async def get_user_tickets(
        self,
        user_id: str = None,
    ) -> list[schemas.UserTicketDetailResponse]:
        user_tickets = await self._repository.get_user_tickets(
            user_id, fetch_links=True
        )
        return user_tickets

    async def get_checked_in_users(
        self,
        event_id: str,
    ) -> List[schemas.CheckedInUserResponse]:
        query = await self._repository.get_checked_in_users_query(event_id)
        user_tickets = await query.to_list()

        ticket_response_list = []
        for user_ticket in user_tickets:
            ticket_response = schemas.CheckedInUserResponse(
                ticket_id=str(user_ticket.id),
                ticket_owner_name=f"{user_ticket.user.first_name} {user_ticket.user.last_name}",
                quantity=user_ticket.quantity,
                email=user_ticket.user.email,
                check_in_date=user_ticket.checked_in_date,
            )
            ticket_response_list.append(ticket_response)
        return ticket_response_list
