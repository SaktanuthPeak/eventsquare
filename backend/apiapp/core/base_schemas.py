"""
Base schemas for the application
"""

from beanie import PydanticObjectId
from pydantic import BaseModel, Field
from datetime import UTC, datetime
from typing import Optional, TypeVar, Union


T = TypeVar("T", bound="BaseSchema")


class BaseSchema(BaseModel):
    id: Optional[Union[PydanticObjectId, str]] = Field(default=None)


class TimestampMixin(BaseModel):
    """Mixin for timestamp fields"""

    created_at: datetime
    updated_at: Optional[datetime] = None


class ErrorResponse(BaseModel):
    """Standard error response"""

    detail: str
    code: Optional[str] = None
    timestamp: datetime = lambda: datetime.now(UTC)


class SuccessResponse(BaseModel):
    """Standard success response"""

    message: str
    data: Optional[dict] = None
