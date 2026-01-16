import datetime
import typing as t
from pydantic import BaseModel, EmailStr, Field
from beanie import PydanticObjectId
from typing import Optional
import uuid


class TicketTypeBase(BaseModel):
    name: str
    total: int
    price: int
    remaining: int


class TicketTypeInput(TicketTypeBase):
    pass


class TicketTypeDB(TicketTypeBase):
    ticket_id: str = Field(default_factory=lambda: str(uuid.uuid4()))


class EventBase(BaseModel):
    name: str
    image_id: Optional[PydanticObjectId] = None
    description: Optional[str]
    event_type: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    booking_start_date: datetime.datetime
    booking_end_date: datetime.datetime


class EventCreate(EventBase):
    ticket_types: Optional[t.List[TicketTypeInput]] = None


class EventUpdate(BaseModel):
    name: Optional[str]
    image_id: Optional[PydanticObjectId]
    description: Optional[str]
    event_type: Optional[str]
    start_date: Optional[datetime.datetime]
    end_date: Optional[datetime.datetime]
    booking_start_date: Optional[datetime.datetime]
    booking_end_date: Optional[datetime.datetime]
    ticket_types: Optional[t.List[TicketTypeInput]] = None


class EventResponse(EventBase):
    id: PydanticObjectId
    ticket_types: t.List[TicketTypeDB] = []
