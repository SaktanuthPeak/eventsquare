"""
User Beanie document model
"""

from beanie import Document, Indexed
from pydantic import Field, field_validator
from typing import Annotated, Optional
from datetime import UTC, datetime
from .schemas import BaseUser
from ...core.base_schemas import TimestampMixin


class User(BaseUser, TimestampMixin, Document):
    """
    User document model for MongoDB collection
    """

    username: Annotated[str, Indexed(unique=True)]
    hashed_password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: Optional[datetime] = None

    @field_validator("username")
    @classmethod
    def normalize_username(cls, v: str) -> str:
        """Normalize username to lowercase for case-insensitive uniqueness"""
        return v.lower().strip() if v else v

    def __str__(self) -> str:
        return f"User(id={self.id})"

    def set_password(self, password: str) -> None:
        """
        Set the user's password after hashing it.
        This method should be called before saving the user document.
        """
        from werkzeug.security import generate_password_hash

        self.hashed_password = generate_password_hash(password)

    def verify_password(self, password: str) -> bool:
        """
        Verify the provided password against the stored hashed password.
        Returns True if the password matches, False otherwise.
        """
        from werkzeug.security import check_password_hash

        return check_password_hash(self.hashed_password, password)

    class Settings:
        name = "users"
