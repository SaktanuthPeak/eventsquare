from bson import ObjectId
from beanie import Document

from .. import models, schemas
from .base_repo import BaseRepository
from api_app.api.core.exceptions import ValidationError

from loguru import logger
from ..utils.schema import PydanticObjectId
from fastapi_pagination.ext.beanie import paginate as beanie_paginate
from fastapi_pagination import Page, Params


class ImageRepository(BaseRepository):
    def __init__(self):
        super().__init__(models.Image)
