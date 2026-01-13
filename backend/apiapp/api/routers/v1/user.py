import typing as t

from fastapi import APIRouter, Depends


from apiapp import models
from apiapp.api.utils.dependencies import get_current_active_user, CurrentUserWithPermission

# from api.core.exceptions import AuthError
from apiapp.services.user_service import UserService
from apiapp.schemas.user_schema import (
    CreateUser,
    User,
    FindUser,
    UserDetail,
    UpdateUser,
    ResetPassword,
    ChangeUserPassword,
)
from fastapi import Request
from fastapi_pagination import Page
from fastapi_pagination.ext.mongoengine import paginate

# from loguru import logger


router = APIRouter(prefix="/users", tags=["users"])


@router.post("")
async def create(
    request: Request,
    user: CreateUser,
    current_user: t.Annotated[
        models.User, Depends(CurrentUserWithPermission("user:create"))
    ],
    service: t.Annotated[UserService, Depends(UserService)],
) -> User:
    return service.create(request, user, current_user)


@router.get("")
async def all(
    current_user: t.Annotated[models.User, Depends(get_current_active_user)],
    service: t.Annotated[UserService, Depends(UserService)],
    find_user: FindUser = Depends(),
) -> Page[User]:
    users = service.find_user(find_user)
    return paginate(users)


@router.get("/{user_id}")
async def get_by_id(
    user_id: str,
    request: Request,
    current_user: t.Annotated[models.User, Depends(get_current_active_user)],
    service: t.Annotated[UserService, Depends(UserService)],
) -> UserDetail:
    return service.get_by_id(user_id)


@router.patch("/{user_id}")
async def patch(
    request: Request,
    current_user: t.Annotated[models.User, Depends(get_current_active_user)],
    user_id: str,
    user: UpdateUser,
    service: t.Annotated[UserService, Depends(UserService)],
) -> UserDetail:
    return service.patch(request, user_id, user, current_user)


@router.put("/{user_id}")
async def update(
    request: Request,
    current_user: t.Annotated[models.User, Depends(get_current_active_user)],
    user_id: str,
    user: UpdateUser,
    service: t.Annotated[UserService, Depends(UserService)],
) -> UserDetail:
    return service.update(request, user_id, user, current_user)


@router.delete("/{user_id}")
async def delete(
    current_user: t.Annotated[
        models.User, Depends(CurrentUserWithPermission("user:delete"))
    ],
    user_id: str,
    service: t.Annotated[UserService, Depends(UserService)],
) -> UserDetail:
    return service.delete_by_id(user_id)


@router.delete("/{user_id}/disactive")
async def disactive(
    request: Request,
    current_user: t.Annotated[
        models.User, Depends(CurrentUserWithPermission("user:delete"))
    ],
    user_id: str,
    service: t.Annotated[UserService, Depends(UserService)],
) -> UserDetail:
    return service.disactive_by_id(request, user_id, current_user)
