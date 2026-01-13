import datetime
import typing as t
from loguru import logger

from ..api.core.config import settings
from ..api.core.exceptions import AuthError
from ..api.core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
    decode_jwt,
)

from .. import models
from ..repositories import UserRepository
from ..schemas import (
    Payload,
    SignIn,
    SignInResponse,
    AccessTokenResponse,
    RefreshToken,
)
from ..services.base_service import BaseService


class AuthService(BaseService):
    def __init__(self):
        user_repository = UserRepository()
        super().__init__(user_repository)

    def login(self, sign_in_info: SignIn) -> SignInResponse:
        user: models.User = self._repository.get_by_options(
            username=sign_in_info.username
        ).first()
        logger.debug("login")
        logger.debug(sign_in_info.username)

        if not user:
            raise AuthError(detail="Incorrect username or password")

        if user.status != "active":
            raise AuthError(detail="Account is not active")

        if not user.verify_password(sign_in_info.password):
            raise AuthError(detail="Incorrect username or password")

        user = self._repository.update_attr(
            user.id, attr="last_login_date", value=datetime.datetime.now()
        )
        delattr(user, "password")

        payload = Payload(**user.to_mongo())
        token = self.generate_user_token(payload)
        self._repository.create_or_update_token(user, token)
        access_token_expires_in = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        return SignInResponse(
            user_info=user,
            access_token_expires_in=access_token_expires_in,
            **token
        )

    def sign_in(self, sign_in_info: SignIn) -> SignInResponse:
        user: models.User = self._repository.get_by_options(
            username=sign_in_info.username
        ).first()
        logger.debug("sign_in")
        logger.debug(user)

        if not user:
            raise AuthError(detail="Incorrect username or password")

        if user.status != "active":
            raise AuthError(detail="Account is not active")

        if not verify_password(sign_in_info.password, user.password):
            raise AuthError(detail="Incorrect username or password")

        user = self._repository.update_attr(
            user.id, attr="last_login_date", value=datetime.datetime.now()
        )
        delattr(user, "password")

        payload = Payload(**user.to_mongo())
        token = self._repository.update_token(
            user, self.generate_user_token(payload)
        )
        return SignInResponse(user_info=user, **token.to_mongo())

    def revoke_longlife_token(self, user_id: str) -> SignInResponse:
        user: models.User = self._repository.get_by_options(id=user_id).firt()

        if not user:
            raise AuthError(detail="Incorrect username or password")

        if user.status != "active":
            raise AuthError(detail="Account is not active")

        user = self._repository.update_attr(
            user.id, attr="last_login_date", value=datetime.datetime.now()
        )
        delattr(user, "password")

        payload = Payload(**user.to_mongo())
        token = self.generate_longlife_user_token(payload)
        self._repository.create_or_update_token(user, token)
        access_token_expires_in = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 30 * 24 * 60
        return SignInResponse(
            user_info=user,
            access_token_expires_in=access_token_expires_in,
            **token
        )

    # def sign_up(
    #     self,
    #     user_info: SignUp,
    #     current_user: models.User,
    # ) -> models.User:
    #     user_info.password = get_password_hash(user_info.password)

    #     if current_user.status != "active":
    #         raise ValidationError(detail="User has not complete sign-up")

    #     signed_up_user = self._repository.get_unique_username(username=user_info.username)
    #     if not signed_up_user:
    #         signed_up_user = self._repository.create(user_info, **user_info.model_dump())
    #     delattr(signed_up_user, "password")
    #     return signed_up_user

    def generate_user_token(self, payload: Payload) -> dict[str, t.Any]:
        access_token_lifespan = datetime.timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        refresh_token_lifespan = datetime.timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )
        access_token, access_token_expires = create_access_token(
            payload.model_dump(), access_token_lifespan
        )
        refresh_token, refresh_token_expires = create_refresh_token(
            payload.model_dump(), refresh_token_lifespan
        )
        access_refresh_token = {
            "access_token": access_token,
            "access_token_expires": access_token_expires,
            "refresh_token": refresh_token,
            "refresh_token_expires": refresh_token_expires,
        }
        return access_refresh_token

    def get_refresh_token(self, refresh_token: RefreshToken) -> AccessTokenResponse:
        if refresh_token.grant_type != "refresh_token":
            raise AuthError("Invalid token or expired token.")

        try:
            token_data = decode_jwt(refresh_token)
            payload = Payload(**token_data)
        except Exception:
            raise AuthError("Could not validate credentials")

        user = self._repository.get_by_id(payload.id)
        user_token = self._repository.get_token(user)

        if (
            token_data["exp"]
            < int(round(datetime.datetime.now(datetime.UTC).timestamp()))
            or user_token.refresh_token_expires.timestamp() != token_data["exp"]
        ):
            raise AuthError("Invalid token or expired token.")

        user_token = self.generate_user_token(payload)
        self._repository.create_or_update_token(user, user_token)

        return user_token

    def generate_longlife_user_token(self, payload: Payload) -> dict[str, t.Any]:
        access_token_lifespan = datetime.timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 30 * 24
        )
        refresh_token_lifespan = datetime.timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES * 30 * 24
        )
        access_token, access_token_expires = create_access_token(
            payload.model_dump(), access_token_lifespan
        )
        refresh_token, refresh_token_expires = create_refresh_token(
            payload.model_dump(), refresh_token_lifespan
        )
        access_refresh_token = {
            "access_token": access_token,
            "access_token_expires": access_token_expires,
            "refresh_token": refresh_token,
            "refresh_token_expires": refresh_token_expires,
        }
        return access_refresh_token
