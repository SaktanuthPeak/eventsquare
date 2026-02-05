import typing as t
from fastapi import APIRouter, Depends, HTTPException, Request, status
from redis.asyncio import Redis

from api_app import schemas, models
from api_app.services import UserTicketService
from ...core import dependencies
from ...core.redis import get_redis
from beanie.operators import Set
from beanie import PydanticObjectId
import datetime
from loguru import logger
from fastapi_pagination import Page, paginate, Params


router = APIRouter(prefix="/user_tickets", tags=["user_tickets"])


@router.get("/{user_ticket_id}")
async def get_user_ticket_by_id(
    user_ticket_id: str,
    current_user: models.User = Depends(dependencies.get_current_user),
    service: UserTicketService = Depends(UserTicketService),
) -> schemas.UserTicketDetailResponse:
    user_ticket = await service.get_user_ticket_by_id(user_ticket_id)
    if not user_ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User ticket not found",
        )
    return user_ticket


@router.get("")
async def get_user_tickets(
    user_id: str = None,
    current_user: models.User = Depends(dependencies.get_current_user),
    service: UserTicketService = Depends(UserTicketService),
) -> list[schemas.UserTicketDetailResponse]:
    user_tickets = await service.get_user_tickets(user_id)
    return user_tickets
