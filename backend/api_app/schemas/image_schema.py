import datetime
import typing as t
from pydantic import BaseModel, EmailStr, Field
from beanie import PydanticObjectId
from typing import Optional
import uuid


class FilePath(BaseModel):
    file_name: str
    content_type: str
    file_id: PydanticObjectId


class ImageFileBase(BaseModel):
    file_path: Optional[FilePath] = None
    content_type: str
    upload_date: datetime.datetime = Field(default_factory=datetime.datetime.now)


class EventImageCreate(BaseModel):
    event_id: PydanticObjectId


class ImageUploadResponse(BaseModel):
    id: PydanticObjectId
    document_id: PydanticObjectId
    file_path: FilePath
    content_type: str
    upload_date: datetime.datetime
