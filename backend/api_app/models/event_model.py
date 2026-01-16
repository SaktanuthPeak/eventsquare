import datetime

from .. import schemas

from beanie import Document
from pydantic import Field


class Event(schemas.EventBase, Document):
    ticket_types: list[schemas.TicketTypeDB] = Field(default_factory=list)
    created_date: datetime.datetime = Field(default_factory=datetime.datetime.now)

    class Settings:
        name = "events"
