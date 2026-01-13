import datetime
import typing as t
from loguru import logger
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordRequestForm,
)

from ...core import security
from ...core.config import settings
from ..user.model import User
from ..user.repository import UserRepository, get_user_repository
from ..user.schemas import UserResponse
from . import schemas
from ...core.base_use_case import BaseUseCase



class AuthUseCase(BaseUseCase[User, UserRepository, UserResponse]):
    def __init__(self, repository: UserRepository):
        super().__init__(repository, UserResponse)


    async def login_for_access_token(
        self,
        form_data: t.Annotated[OAuth2PasswordRequestForm, Depends()],
    ) -> schemas.GetAccessTokenResponse:
        user = await self.repository.find_one(
            filters={"username": form_data.username, "is_active": True}
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = datetime.timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        access_token = security.jwt_handler.create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    
    async def authentication(
        self,
        form_data: t.Annotated[OAuth2PasswordRequestForm, Depends()],
    ) -> schemas.Token:
        user = await self.repository.find_one(
            filters={"username": form_data.username, "is_active": True}
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )

        if not user.verify_password(form_data.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )

        await self.repository.update(
            entity_id=user.id, update_data={"last_login_date": datetime.datetime.now()}
        )

        print(user.last_login_date)

        access_token_expires = datetime.timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        refresh_token_expires = datetime.timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )
        return schemas.Token(
            access_token=security.jwt_handler.create_access_token(
                data={"sub": str(user.id), "token_type": "access"},
                expires_delta=access_token_expires,
            ),
            refresh_token=security.jwt_handler.create_refresh_token(
                data={"sub": str(user.id), "token_type": "refresh"},
                expires_delta=refresh_token_expires,
            ),
            token_type="Bearer",
            scope="",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            expires_at=datetime.datetime.now() + access_token_expires,
            issued_at=user.last_login_date,
        )

    async def refresh_token(
        credentials: t.Annotated[HTTPAuthorizationCredentials, Security(HTTPBearer())],
    ) -> schemas.GetAccessTokenResponse:
        refresh_token_str = credentials.credentials

        try:
            new_access_token = security.jwt_handler.refresh_token(refresh_token_str)
            return {"access_token": new_access_token, "token_type": "bearer"}
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Exception in: {e}",
            )

    
# Dependency providers
async def get_auth_use_case(
    repository: UserRepository = Depends(get_user_repository),
) -> AuthUseCase:
    """Get user use case with injected dependencies"""
    return AuthUseCase(repository)