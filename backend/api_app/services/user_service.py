from fastapi import (
    Request,
)

from api_app.api.core.security import get_password_hash, verify_password
from api_app.api.core.exceptions import AuthError
from ..repositories import UserRepository
from api_app.api.core.exceptions import ValidationError, NotFoundError

from .. import models, schemas
from ..services import BaseService

from ..utils import request_logs as rl

from loguru import logger


class UserService(BaseService):
    def __init__(self):
        user_repository = UserRepository()
        super().__init__(user_repository)

    async def get_list_with_paginate(
        self,
        schema: schemas.FindUser,
        current_page: int = 1,
        limit: int = 50,
    ) -> schemas.UserList:

        schema_dict = schema.model_dump(exclude_defaults=True)
        query_schema_dict = {}
        if "username" in schema_dict:
            query_schema_dict["username"] = {
                "$regex": schema_dict.pop("username"),
                "$options": "i",
            }

        if "email" in schema_dict:
            query_schema_dict["email"] = {
                "$regex": schema_dict.pop("email"),
                "$options": "i",
            }

        users = await self.get_list(**query_schema_dict, **schema_dict)
        count = 0

        count = len(users)
        start = (current_page - 1) * limit
        end = start + limit
        paginated_users = users[start:end]

        # Calculate total pages
        if count % limit == 0 and count // limit > 0:
            total_page = count // limit
        else:
            total_page = (count // limit) + 1

        return schemas.UserList(
            users=list(paginated_users),
            count=count,
            current_page=current_page,
            total_page=total_page,
        )
