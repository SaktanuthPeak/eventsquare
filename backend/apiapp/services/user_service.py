from fastapi import (
    Request,
)

from ..api.core.security import get_password_hash, verify_password
from ..api.core.exceptions import AuthError
from ..schemas import (
    ChangeUserPassword,
    ResetPassword,
    CreateUser,
    UpdateUser,
)
from ..repositories import UserRepository
from ..api.core.exceptions import ValidationError, NotFoundError

from .. import models
from ..services import BaseService

from ..schemas.user_schema import FindUser

from ..utils import request_logs as rl
from bson import ObjectId


class UserService(BaseService):
    def __init__(self):
        user_repository = UserRepository()
        super().__init__(user_repository)

    def change_password(
        self, current_user: models.User, password_info: ChangeUserPassword
    ) -> models.User:
        if not verify_password(password_info.current_password, current_user.password):
            raise AuthError(detail="Incorrect current password")

        password = get_password_hash(password_info.new_password)
        user = self._repository.update_attr(
            current_user.id, attr="password", value=password
        )

        return user

    def reset_password(self, user_id, reset_password: ResetPassword) -> models.User:
        found_user = self._repository.get_by_id(user_id)
        password = get_password_hash(reset_password.new_password)
        user = user = self._repository.update_attr(
            found_user.id, attr="password", value=password
        )
        return user

    def create(
        self,
        request: Request,
        schema: CreateUser,
        current_user: models.User,
    ) -> models.User:
        schema.password = get_password_hash(schema.password)

        if current_user.status != "active":
            raise ValidationError(detail="User has not complete sign-up")

        signed_up_user = self._repository.get_unique_username(username=schema.username)
        if not signed_up_user:
            request_log = rl.create_logs(
                action="create", request=request, current_user=current_user
            )

            schema_dict = schema.model_dump(exclude_defaults=True)

            signed_up_user = self._repository.create(
                request_log=request_log, **schema_dict
            )

        delattr(signed_up_user, "password")
        return signed_up_user

    def find_user(self, schema: FindUser) -> list[models.User]:
        schema_dict = schema.model_dump(exclude_defaults=True)
        query_schema_dict = {}
        if "first_name" in schema_dict:
            query_schema_dict["first_name__icontains"] = schema_dict.pop("first_name")
        if "last_name" in schema_dict:
            query_schema_dict["last_name__icontains"] = schema_dict.pop("last_name")
        if "username" in schema_dict:
            query_schema_dict["username__icontains"] = schema_dict.pop("username")
        if "email" in schema_dict:
            query_schema_dict["email__icontains"] = schema_dict.pop("email")

        return self.get_list(**query_schema_dict, **schema_dict)

    def patch(
        self,
        request: Request,
        user_id: str,
        schema: UpdateUser,
        current_user: models.User,
    ) -> models.User:
        request_log = rl.create_logs(
            action="update", request=request, current_user=current_user
        )
        schema_dict = schema.model_dump(exclude_defaults=True)

        user = self._repository.update(user_id, request_log=request_log, **schema_dict)
        return user

    def update(
        self,
        request: Request,
        user_id: str,
        schema: UpdateUser,
        current_user: models.User,
    ) -> models.User:
        request_log = rl.create_logs(
            action="update", request=request, current_user=current_user
        )
        schema_dict = schema.model_dump()

        user = self._repository.update(user_id, request_log=request_log, **schema_dict)
        return user

    def disactive_by_id(
        self,
        request: Request,
        user_id: str,
        current_user: models.User,
    ) -> models.User:
        request_log = rl.create_logs(
            action="disactive", request=request, current_user=current_user
        )
        return self._repository.disactive_by_id(user_id, request_log=request_log)
