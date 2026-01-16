import typing as t
from fastapi import Depends
from pydantic import ValidationError
from loguru import logger

from ..core.exceptions import AuthError, NoPermission
from ..core.security import JWTBearer, reusable_oauth2, decode_jwt

from api_app import models
from api_app.services.user_service import UserService
from api_app.schemas.auth_schema import Payload


def get_current_user(token: t.Annotated[str, Depends(reusable_oauth2)]) -> models.User:
    service = UserService()
    try:
        payload = decode_jwt(token)
        token_data = Payload(**payload)
    except ValidationError as e:
        logger.error(str(e))
        raise AuthError(detail="Could not validate credentials")

    current_user: models.User = service.get_by_id(token_data.id)
    if not current_user:
        raise AuthError(detail="User not found")

    return current_user


def get_current_active_user(
    current_user: t.Annotated[models.User, Depends(get_current_user)],
) -> models.User:
    if not current_user.status == "active":
        raise NoPermission("Inactive user")

    return current_user


def get_current_user_with_no_exception(
    token: t.Annotated[str, Depends(JWTBearer())],
    service: t.Annotated[UserService, Depends(UserService)],
) -> models.User | None:
    try:
        payload = decode_jwt(token)
        token_data = Payload(**payload)
    except Exception:
        return None

    current_user: models.User = service.get_by_id(token_data.id)
    if not current_user:
        return None

    return current_user


def get_current_admin_user(
    current_user: t.Annotated[models.User, Depends(get_current_user)],
) -> models.User:
    if current_user.status != "active":
        raise NoPermission("Inactive user")

    if "admin" not in current_user.p:
        raise NoPermission("User is not admin")

    return current_user


def get_current_user_with_roles(
    current_user: t.Annotated[models.User, Depends(get_current_user)],
    roles: tuple | list[str] = ["user"],
) -> models.User:
    """
    :param roles: default value ["user"], example ["admin", "staff"]
    """
    if roles and not isinstance(roles, (list, tuple)):
        raise TypeError()

    if current_user.status != "active":
        raise NoPermission("Inactive user")

    for role in roles:
        if role in current_user.roles:
            return current_user

    raise NoPermission(f"User is not role {role}")


class CurrentUserWithPermission:
    def __init__(self, *allow_permissions: tuple[str]):
        self.allow_permissions = allow_permissions

    def __call__(
        self, current_user: t.Annotated[models.User, Depends(get_current_active_user)]
    ) -> models.User | NoPermission:
        role_ids = [role.id for role in current_user.organization_roles]

        role = models.OrganizationRole.objects(
            permissions__name__in=self.allow_permissions, id__in=role_ids
        ).first()

        if role:
            return current_user
        raise NoPermission("User is not role permission")
