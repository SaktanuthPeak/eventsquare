import datetime
import typing as t
from pydantic import BaseModel, EmailStr, Field
from beanie import PydanticObjectId
from typing import Optional
import uuid
from beanie import Link
from api_app import schemas


class BaseUserTicket(BaseModel):
    user = Link[schemas.User]
    event = Link[schemas.EventResponse]
    ticket_name: str
    price: int
    status: str
    event_start_date: datetime.datetime
    event_end_date: datetime.datetime
    purchase_date: datetime.datetime = Field(default_factory=datetime.datetime.now)
    created_date: datetime.datetime = Field(default_factory=datetime.datetime.now)
    is_checked_in: bool = Field(default=False)
    checked_in_date: datetime.datetime | None = Field(default=None)
    status: str = Field(default="active")


class UserTicketCreate(BaseUserTicket):
    pass
