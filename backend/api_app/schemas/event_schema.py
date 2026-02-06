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
    location: Optional[str] = None
    start_date: datetime.datetime
    end_date: datetime.datetime
    booking_start_date: datetime.datetime
    booking_end_date: datetime.datetime
    created_by: Optional[PydanticObjectId] = None


class EventCreate(BaseModel):
    name: str
    description: Optional[str]
    event_type: str
    location: Optional[str] = None
    ticket_types: Optional[t.List[TicketTypeInput]] = None
    start_date: datetime.datetime
    end_date: datetime.datetime
    booking_start_date: datetime.datetime
    booking_end_date: datetime.datetime


class EventUpdate(BaseModel):
    name: Optional[str] = None
    image_id: Optional[PydanticObjectId] = None
    description: Optional[str] = None
    location: Optional[str] = None
    event_type: Optional[str] = None
    start_date: Optional[datetime.datetime] = None
    end_date: Optional[datetime.datetime] = None
    booking_start_date: Optional[datetime.datetime] = None
    booking_end_date: Optional[datetime.datetime] = None
    ticket_types: Optional[t.List[TicketTypeInput]] = None


class EventResponse(EventBase):
    id: PydanticObjectId
    ticket_types: t.List[TicketTypeDB] = []


class EventSearch(BaseModel):
    name: Optional[str] = Field(None, example="Music Festival")
    event_type: Optional[str] = Field(None, example="concert")
    start_date_from: Optional[str] = Field(None, example="2025-01-01")
    start_date_to: Optional[str] = Field(None, example="2025-01-01")


class TicketBooking(BaseModel):
    event_id: str = Field(..., description="Event ID")
    ticket_type_name: str = Field(..., description="Ticket name")
    ticket_type_id: str = Field(..., description="Ticket type ID")
    quantity: int = Field(
        ..., gt=0, le=10, description="Number of tickets (max 10 per booking)"
    )
    price_per_ticket: int = Field(..., description="Price per ticket")
    total_price: int = Field(..., description="Total price for the booking")


class TicketPayloadSchema(BaseModel):
    event_name: str = Field(..., description="Name of the event")
    ticket_type_name: str = Field(..., description="Name of the ticket type")
    quantity: int = Field(..., description="Number of tickets booked")
    total_price: int = Field(..., description="Total price for the booked tickets")
    price_per_ticket: int = Field(..., description="Price per ticket")
    email: str
    first_name: str
    last_name: str
