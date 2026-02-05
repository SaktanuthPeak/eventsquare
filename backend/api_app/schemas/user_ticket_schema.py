import datetime
import typing as t
from pydantic import BaseModel, EmailStr, Field
from beanie import PydanticObjectId
from typing import Optional
import uuid
from beanie import Link
from api_app import schemas


class BaseUserTicket(BaseModel):
    user_id: PydanticObjectId
    event_id: PydanticObjectId
    ticket_type_id: str
    ticket_name: str
    quantity: int
    price_per_ticket: int
    total_price: int
    event_start_date: datetime.datetime
    event_end_date: datetime.datetime
    purchase_date: datetime.datetime = Field(default_factory=datetime.datetime.now)
    is_checked_in: bool = Field(default=False)
    checked_in_date: Optional[datetime.datetime] = Field(default=None)
    status: str = Field(default="active")


# Create schema
class UserTicketCreate(BaseUserTicket):
    pass


# Response schema (basic)
class UserTicketResponse(BaseUserTicket):
    id: PydanticObjectId


class UserTicketDetailResponse(BaseModel):
    id: PydanticObjectId
    ticket_type_id: str
    ticket_name: str
    quantity: int
    price_per_ticket: int
    total_price: int
    event_start_date: datetime.datetime
    event_end_date: datetime.datetime
    purchase_date: datetime.datetime
    is_checked_in: bool
    checked_in_date: Optional[datetime.datetime]
    status: str
    user: Optional[schemas.User] = None
    event: Optional[schemas.EventResponse] = None
