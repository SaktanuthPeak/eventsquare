import typing as t
from fastapi import APIRouter, Depends, HTTPException, Request, status
from api_app import schemas, models
from api_app.services import UserService
from ...core import dependencies
from beanie.operators import Set
from beanie import PydanticObjectId
import datetime


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model_by_alias=False, response_model=schemas.User)
def get_me(current_user: models.User = Depends(dependencies.get_current_user)):
    return current_user


@router.get("/{user_id}")
async def get_by_id(
    user_id: str,
    request: Request,
    current_user: models.User = Depends(dependencies.get_current_user),
    service: UserService = Depends(UserService),
) -> schemas.User:
    user = await service.get_by_id(user_id)
    return user


@router.get(
    "",
    response_model_by_alias=False,
)
async def get_all(
    current_page: int = 1,
    limit: int = 50,
    find_user: schemas.FindUser = Depends(),
    current_user: models.User = Depends(dependencies.get_current_user),
    service: UserService = Depends(UserService),
) -> schemas.UserList:
    users = await service.get_list_with_paginate(
        schema=find_user, current_page=current_page, limit=limit
    )
    return users


@router.post(
    "",
    # response_model=schemas.User,
    response_model_by_alias=False,
)
async def create(
    user_register: schemas.RegisteredUser,
) -> schemas.User:
    user = await models.User.find_one(models.User.username == user_register.username)

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This username is exists.",
        )

    user = models.User(**user_register.dict())
    await user.set_password(user_register.password)
    await user.insert()

    return user


@router.patch(
    "/{user_id}/change_password",
    response_model=schemas.User,
    response_model_by_alias=False,
)
def change_password(
    user_id: str,
    password_update: schemas.ChangedPassword,
    current_user: schemas.User = Depends(dependencies.get_current_user),
):
    try:
        user = schemas.User.objects.get(id=user_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found this user",
        )
    if not user.verify_password(password_update.current_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )

    user.set_password(password_update.new_password)
    user.save()
    return user


@router.patch(
    "/{user_id}/update",
    response_model=schemas.User,
    response_model_by_alias=False,
)
def update(
    request: Request,
    user_id: str,
    user_update: schemas.UpdatedUser,
    current_user: schemas.User = Depends(dependencies.get_current_user),
):
    try:
        user = schemas.User.objects.get(id=user_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found this user",
        )

    set_dict = {f"set__{k}": v for k, v in user_update.dict().items() if v is not None}

    user.update(**set_dict)

    user.reload()

    if user.citizen_id:
        user.citizen_id = user.citizen_id.replace("-", "")
    user.save()
    return user


@router.patch(
    "/{user_id}/set_status",
    response_model=schemas.User,
    response_model_by_alias=False,
)
async def set_status(
    user_id: PydanticObjectId,
    status: str = "active",
    current_user: schemas.User = Depends(dependencies.get_current_user),
):
    try:
        user = await models.User.find_one(
            models.User.id == user_id,
            fetch_links=True,
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found this user",
        )
    user.status = status
    # logger.debug(user)
    await user.update(Set(user))
    user.updated_date = datetime.datetime.now()
    await user.save()

    return user


@router.patch(
    "/{user_id}/set_role",
)
async def set_role(
    user_id: PydanticObjectId,
    role: str,
    action: str,
    current_user: schemas.User = Depends(dependencies.get_current_user),
) -> schemas.User:
    try:
        user = await models.User.find_one(
            models.User.id == user_id,
            fetch_links=True,
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found this user",
        )
    data = user.roles

    if action == "add":
        data.append(role)
    elif action == "remove":
        data.remove(role)

    # logger.debug(user)
    await user.update(Set(user))
    user.updated_date = datetime.datetime.now()
    await user.save()

    return user
