from fastapi import (
    Request,
    UploadFile,
    HTTPException,
)
from redis.asyncio import Redis
from typing import Optional
from loguru import logger

from ..repositories import ImageRepository

from .. import models, schemas
from ..services import BaseService
from fastapi_pagination import Page, Params, paginate
from fastapi_pagination.ext.beanie import paginate as beanie_paginate
import datetime
from fastapi.responses import StreamingResponse
from api_app.api.core.gridfs import File
from beanie import PydanticObjectId
import io


class ImageService(BaseService):
    def __init__(self):
        image_repository = ImageRepository()
        super().__init__(image_repository)

    ALLOWED_CONTENT_TYPES = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    MAX_FILE_SIZE = 10 * 1024 * 1024

    async def upload_image(
        self, file: UploadFile, event_id: Optional[str] = None
    ) -> schemas.ImageUploadResponse:
        if file.content_type not in self.ALLOWED_CONTENT_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed types: {', '.join(self.ALLOWED_CONTENT_TYPES)}",
            )

        file_content = await file.read()

        if len(file_content) > self.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File size exceeds maximum limit of {self.MAX_FILE_SIZE / (1024*1024)}MB",
            )

        if event_id:
            event = await models.Event.get(PydanticObjectId(event_id))
            if not event:
                raise HTTPException(status_code=404, detail="Event not found")

        gridfs_file = File(collection_name="images")
        fs = await gridfs_file.get_gridfs()

        file_id = await fs.upload_from_stream(
            file.filename,
            io.BytesIO(file_content),
            metadata={
                "content_type": file.content_type,
                "original_filename": file.filename,
                "upload_date": datetime.datetime.now(),
                "event_id": event_id if event_id else None,
            },
        )

        image = models.Image(
            file_id=file_id,
        )
        await image.insert()

        if event_id:
            event = await models.Event.get(PydanticObjectId(event_id))
            event.image_id = image.id
            await event.save()

        return schemas.ImageUploadResponse(
            id=image.id,
            document_id=file_id,
            file_path=schemas.FilePath(
                file_name=file.filename, content_type=file.content_type, file_id=file_id
            ),
            content_type=file.content_type,
            upload_date=image.created_date,
        )

    async def get_image(self, image_id: str) -> StreamingResponse:
        image = await models.Image.get(PydanticObjectId(image_id))
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")
        gridfs_file = File(collection_name="images")
        fs = await gridfs_file.get_gridfs()
        try:
            grid_out = await fs.open_download_stream(image.file_id)

            metadata = grid_out.metadata or {}
            content_type = metadata.get("content_type", "image/jpeg")
            filename = metadata.get("original_filename", f"image_{image_id}")

            async def stream_file():
                while chunk := await grid_out.read(1024 * 1024):  # Read in 1MB chunks
                    yield chunk

            return StreamingResponse(
                stream_file(),
                media_type=content_type,
                headers={"Content-Disposition": f"inline; filename={filename}"},
            )

        except Exception as e:
            logger.error(f"Error downloading file from GridFS: {e}")
            raise HTTPException(status_code=404, detail="File not found in GridFS")

    async def delete_image(self, image_id: str) -> bool:

        image = await models.Image.get(PydanticObjectId(image_id))
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")
        gridfs_file = File(collection_name="images")
        fs = await gridfs_file.get_gridfs()
        try:
            await fs.delete(image.file_id)
        except Exception as e:
            logger.error(f"Error deleting file from GridFS: {e}")

        await image.delete()

        return True
