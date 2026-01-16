from bson import ObjectId
from beanie import Document

from .. import models, schemas
from .base_repo import BaseRepository
from api_app.api.core.exceptions import ValidationError

from loguru import logger


class EventRepository(BaseRepository):
    def __init__(self):
        super().__init__(models.Event)

    async def get_event_by_id(self, event_id: str) -> Document | None:
        try:
            item = self.model.objects(id=ObjectId(event_id)).first()
        except Exception:
            raise ValidationError(detail="Invalid event ID")

        return item
