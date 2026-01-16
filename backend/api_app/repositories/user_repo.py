from bson import ObjectId
from beanie import Document

from .. import models, schemas
from .base_repo import BaseRepository
from api_app.api.core.exceptions import ValidationError

from loguru import logger


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(models.User)

    async def get_unique_username(self, username: str) -> Document | None:
        try:
            item = self.model.objects(username=username).first()
        except Exception:
            raise ValidationError(detail="Invalid username")

        return item
