"""
User module schemas (DTOs)
"""

from enum import Enum
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional
from datetime import datetime, timezone

from apiapp.core.exceptions import ValidationError

from ...core.base_schemas import BaseSchema


class UserRole(Enum):
    """Enumeration for user roles"""

    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"


class BaseUser(BaseModel):
    """Base schema with common fields for user"""

    username: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Username of the user",
    )
    name: str = Field(..., min_length=1, max_length=100, description="Name of the user")
    email: Optional[str] = Field(
        default=None, max_length=255, description="Email address of the user"
    )
    role: UserRole = Field(
        default=UserRole.USER, description="List of roles assigned to the user"
    )
    is_active: bool = Field(default=True, description="Indicates if the user is active")
    last_login_date: Optional[datetime] = Field(
        default=None, description="Last login date of the user"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Creation timestamp",
    )


class CreateUser(BaseModel):
    username: str = Field(
        ..., min_length=1, max_length=50, description="Username of the user"
    )
    name: str = Field(..., min_length=1, max_length=100, description="Name of the user")
    email: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Email address of the user",
        examples=["user@email.com"],
    )
    password: str = Field(
        ..., min_length=8, max_length=128, description="User password"
    )
    confirm_password: str = Field(
        ..., min_length=8, max_length=128, description="Confirm user password"
    )
    role: str = Field(
        default=UserRole.USER.value, description="Role assigned to the user"
    )

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        if len(v) < 3:
            raise ValidationError("Username must be at least 3 characters long")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValidationError("Password must be at least 8 characters long")
        return v

    @model_validator(mode="after")
    def validate_passwords_match(self):
        """Check that password and confirm_password match"""
        if self.password != self.confirm_password:
            raise ValidationError("Passwords do not match")
        return self


class GetUser(BaseModel):
    search: Optional[str] = Field(
        default=None, description="Search in username, email, or name"
    )
    role: Optional[UserRole] = Field(default=None, description="Filter by user role")
    is_active: Optional[bool] = Field(
        default=None, description="Filter by active status"
    )


class UpdateUser(BaseModel):
    """Schema for updating user data - all fields optional"""

    username: Optional[str] = Field(
        default=None, min_length=1, max_length=50, description="Username of the user"
    )
    name: Optional[str] = Field(
        default=None, min_length=1, max_length=100, description="Name of the user"
    )
    email: Optional[str] = Field(
        default=None, max_length=255, description="Email address of the user"
    )
    role: Optional[UserRole] = Field(
        default=None, description="Role assigned to the user"
    )
    is_active: Optional[bool] = Field(
        default=None, description="Indicates if the user is active"
    )

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        if v is not None and len(v) < 3:
            raise ValidationError("Username must be at least 3 characters long")
        return v


class UserResponse(BaseSchema, BaseUser): ...


class UpdateUserPassword(BaseModel):
    """Schema for updating user password"""

    old_password: str = Field(
        ..., min_length=8, max_length=128, description="Current user password"
    )
    new_password: str = Field(
        ..., min_length=8, max_length=128, description="New user password"
    )
    confirm_new_password: str = Field(
        ..., min_length=8, max_length=128, description="Confirm new user password"
    )

    @model_validator(mode="after")
    def validate_passwords_match(self):
        """Check that new_password and confirm_new_password match"""
        if self.new_password != self.confirm_new_password:
            raise ValidationError("New passwords do not match")
        return self
