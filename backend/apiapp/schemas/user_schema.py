import datetime

import typing as t
from pydantic import Field
from ..schemas.base_schema import BaseSchema, FindBase, BaseSchemaId, SearchOptions


class BaseUser(BaseSchema):
    title_name: str = Field(example="คำนำหน้า")
    first_name: str = Field(example="ชื่อจริง")
    last_name: str = Field(example="นามสกุล")
    status: str = Field(example="สถานะ")


class BaseUserWithPassword(BaseUser):
    password: str = Field(example="รหัสผ่าน")


class User(BaseSchemaId, BaseUser):
    username: str = Field(example="ชื่อบัญชี")
    email: str = Field(example="อีเมล")
    last_login_date: datetime.datetime
    ...


class LoginUserResponse(BaseSchemaId, BaseUser):
    username: str = Field(example="ชื่อบัญชี")
    email: str = Field(example="อีเมล")
    last_login_date: datetime.datetime
    ...


class FindUser(FindBase, BaseUser):
    title_name: t.Optional[str] = Field(None, example="คำนำหน้า")
    first_name: t.Optional[str] = Field(None, example="ชื่อจริง")
    last_name: t.Optional[str] = Field(None, example="นามสกุล")
    username: t.Optional[str] = Field(None, example="ชื่อบัญชี")
    status: t.Optional[str] = Field(None, example="สถานะ")
    email: t.Optional[str] = Field(None, example="test@example.com")
    roles: t.Optional[str] = Field(None, example="บทบาท")


class UpsertUser(BaseUser): ...


class FindUserResult(BaseSchema):
    founds: t.Optional[t.List[User]]
    search_options: t.Optional[SearchOptions]


class ChangeUserPassword(BaseSchema):
    current_password: str = Field(example="รหัสผ่าน")
    new_password: str = Field(example="รหัสผ่านใหม่")


class ResetPassword(BaseSchema):
    new_password: str = Field(example="รหัสผ่านใหม่")


class CreateUser(BaseSchema):
    username: str = Field(example="ชื่อบัญชี")
    password: str = Field(example="รหัสผ่าน")
    email: t.Optional[str] = Field(None, example="test@example.com")
    title_name: str = Field(example="คำนำหน้า")
    first_name: str = Field(example="ชื่อจริง")
    last_name: str = Field(example="นามสกุล")


class UserDetail(User):
    roles: list[str]


class UpdateUser(BaseSchema):
    title_name: str = Field(example="คำนำหน้า")
    first_name: str = Field(example="ชื่อจริง")
    last_name: str = Field(example="นามสกุล")
