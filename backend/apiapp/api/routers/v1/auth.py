import typing as t

from fastapi import APIRouter, Depends
from fastapi.security import (
    OAuth2PasswordRequestForm,
)

from ...utils.dependencies import get_current_active_user

from .... import models
from ....schemas.user_schema import LoginUserResponse
from ....services.auth_service import AuthService
from ....schemas.auth_schema import (
    SignIn,
    SignInResponse,
    # SignUp,
    AccessTokenResponse,
    RefreshToken,
)
from loguru import logger


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/login",
)
async def authentication(
    auth_service: t.Annotated[AuthService, Depends(AuthService)],
    form_data: t.Annotated[
        OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)
    ],
    name="auth:login",
) -> SignInResponse:
    logger.debug("in login route")
    login_info = SignIn(username=form_data.username, password=form_data.password)
    auth_service_login = auth_service.login(login_info)

    return auth_service_login


@router.post("/sign-in", response_model=SignInResponse)
async def sign_in(
    user_info: SignIn, auth_service: t.Annotated[AuthService, Depends(AuthService)]
):
    return auth_service.sign_in(user_info)


# @router.post("/sign-up", response_model=User)
# async def sign_up(
#     user_info: SignUp,
#     current_user: models.User = Depends(get_current_active_user),
#     auth_service: AuthService = Depends(AuthService),
# ):
#     return auth_service.sign_up(user_info, current_user)


@router.get("/me", response_model=LoginUserResponse)
async def get_me(
    current_user: t.Annotated[models.User, Depends(get_current_active_user)]
):
    return current_user


@router.post("/refresh_token", response_model=AccessTokenResponse)
async def refresh_token(
    refresh_token: RefreshToken,
    auth_service: t.Annotated[AuthService, Depends(AuthService)],
):
    return auth_service.get_refresh_token(refresh_token)
