from fastapi import (
    Request,
)

from api_app.api.core.security import get_password_hash, verify_password
from api_app.api.core.exceptions import AuthError
from ..repositories import EventRepository
from api_app.api.core.exceptions import ValidationError, NotFoundError

from .. import models, schemas
from ..services import BaseService

from ..utils import request_logs as rl

from loguru import logger


class EventService(BaseService):
    def __init__(self):
        event_repository = EventRepository()
        super().__init__(event_repository)

    async def get_event_by_id(
        self,
        event_id: str,
    ) -> schemas.EventResponse:

        event = await self._repository.get_event_by_id(event_id)

        return event
