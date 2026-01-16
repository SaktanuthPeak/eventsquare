import datetime

import typing as t

from pydantic import Field

from .user_schema import LoginUserResponse
from .base_schema import BaseSchema
from ..utils.schema import PydanticObjectId


class TokenResponse(BaseSchema):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    expires_at: datetime.datetime
    scope: str
    issued_at: datetime.datetime


class SignIn(BaseSchema):
    username: str
    password: str


class Payload(BaseSchema):
    id: PydanticObjectId = Field(alias="_id", serialization_alias="id")
    roles: t.List[str]


class AccessTokenResponse(BaseSchema):
    access_token: str
    access_token_expires: datetime.datetime
    refresh_token: str
    refresh_token_expires: datetime.datetime


class SignInResponse(AccessTokenResponse):
    user_info: LoginUserResponse
    access_token_expires_in: int
    ...


class RefreshToken(BaseSchema):
    grant_type: str
    refresh_token: str
