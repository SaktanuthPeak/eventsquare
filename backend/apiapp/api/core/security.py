import datetime
import bcrypt
import json
from jwcrypto import jwt, jwk

from fastapi import Request
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordBearer,
)
from loguru import logger

from ..core.config import settings
from ..core.exceptions import AuthError
from ...repositories.user_repo import UserRepository

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
ALGORITHM = ("HS256", "A256KW")
JWT_HEADER = {"alg": ALGORITHM[0]}
JWE_HEADER = {"alg": ALGORITHM[1], "enc": "A256CBC-HS512"}


def create_access_token(
    subject: dict, expires_delta: datetime.timedelta = None
) -> tuple[str, str]:
    if expires_delta:
        expire = datetime.datetime.now(datetime.UTC) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    payload = {"exp": int(expire.timestamp()), **subject}
    encoded_jwt = encode_jwt(payload)
    # expiration_datetime = str(int(expire.timestamp()))
    expiration_datetime = expire
    return encoded_jwt, expiration_datetime


def create_refresh_token(
    subject: dict, expires_delta: datetime.timedelta = None
) -> tuple[str, str]:
    if expires_delta:
        expire = datetime.datetime.now(datetime.UTC) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )

    payload = {"exp": int(expire.timestamp()), **subject}
    encoded_jwt = encode_jwt(payload)
    # expiration_datetime = str(int(expire.timestamp()))
    expiration_datetime = expire
    return encoded_jwt, expiration_datetime


def get_jwt_key():
    logger.debug(len(settings.SECRET_KEY))
    if len(settings.SECRET_KEY) != 43:
        logger.error("SECRET_KEY length should be 43")
        raise Exception("SECRET_KEY length should be 43")

    k = {"k": settings.SECRET_KEY, "kty": "oct"}
    jwt_key = jwk.JWK(**k)

    return jwt_key


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(14)).decode()


def encode_jwt(payload: dict) -> bytes:
    try:
        key = get_jwt_key()
        Token = jwt.JWT(header=JWT_HEADER, claims=payload)
        Token.make_signed_token(key)
        Etoken = jwt.JWT(header=JWE_HEADER, claims=Token.serialize())
        Etoken.make_encrypted_token(key)
        encoded_jwt = Etoken.serialize()
    except Exception:
        raise AuthError("Couldn't encoding Token")

    return encoded_jwt


def decode_jwt(token: str) -> dict:
    try:
        key = get_jwt_key()
        ET = jwt.JWT(key=key, jwt=token, expected_type="JWE")
        ST = jwt.JWT(key=key, jwt=ET.claims)
        decoded_token = json.loads(ST.claims)
        user_token = UserRepository.get_token(decoded_token["id"])
        if decoded_token["exp"] == user_token.access_token_expires.timestamp():
            return decoded_token
        else:
            return {}

    except Exception:
        return {}


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise AuthError(detail="Invalid authentication scheme.")

            if not self.verify_jwt(credentials.credentials):
                raise AuthError(detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise AuthError(detail="Invalid authorization code.")

    def verify_jwt(self, jwt_token: str) -> bool:
        is_token_valid: bool = False
        try:
            payload = decode_jwt(jwt_token)
        except Exception:
            payload = None

        if payload:
            is_token_valid = True

        return is_token_valid
