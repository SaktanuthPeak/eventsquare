from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordRequestForm,
)

import typing

from .schemas import GetAccessTokenResponse


from ...core import security, exceptions
from ...core.config import settings
from .use_case import AuthUseCase, get_auth_use_case
from . import schemas


router = APIRouter(
    prefix="/v1/auth",
    tags=["Authentication"],
)


@router.post(
    "/token",
    summary="Get OAuth2 access token",
)
async def login_for_access_token(
    form_data: typing.Annotated[OAuth2PasswordRequestForm, Depends()],
    use_case: AuthUseCase = Depends(get_auth_use_case)
) -> schemas.GetAccessTokenResponse:
    try:
        return await use_case.login_for_access_token(
            form_data=form_data
        )
    except (exceptions.BusinessLogicError, exceptions.ValidationError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/login",
)
async def authentication(
    form_data: typing.Annotated[OAuth2PasswordRequestForm, Depends()],
    use_case: AuthUseCase = Depends(get_auth_use_case),
    name="auth:login",
) -> schemas.Token:
    try:
        return await use_case.authentication(
            form_data=form_data
        )
    except (exceptions.BusinessLogicError, exceptions.ValidationError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/refresh_token")
async def refresh_token(
    credentials: typing.Annotated[HTTPAuthorizationCredentials, Security(HTTPBearer())],
    use_case: AuthUseCase = Depends(get_auth_use_case)
) -> GetAccessTokenResponse:
    refresh_token_str = credentials.credentials

    try:
        return await use_case.refresh_token(
            credentials=credentials
        )
    except (exceptions.BusinessLogicError, exceptions.ValidationError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
