import datetime
from beanie import Document, Link, PydanticObjectId
from pydantic import Field
from typing import Optional

from api_app.models import User, Event


class UserTicket(Document):
    user: Link[User]
    event: Link[Event]
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

    class Settings:
        name = "user_tickets"
        use_state_management = True
