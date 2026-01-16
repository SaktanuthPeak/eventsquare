from datetime import datetime, timedelta, timezone
import bcrypt
import json

from jwcrypto import jwk
from jose import jwt
from jose.exceptions import JWTError

from fastapi import Request, HTTPException, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordBearer,
)
from loguru import logger

from .config import settings
from .exceptions import AuthError
from ...repositories.user_repo import UserRepository

# reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
ALGORITHM = "HS256"
# JWT_HEADER = {"alg": ALGORITHM[0]}
# JWE_HEADER = {"alg": ALGORITHM[1], "enc": "A256CBC-HS512"}


class JWTHandler:
    def __init__(self, secret_key: str, algorithm: str):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def create_refresh_token(
        self, data: dict, expires_delta: timedelta | None = None
    ) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
            )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def decode_token(self, token: str, token_type: str | None = None) -> dict:
        try:
            decoded_payload = jwt.decode(
                token, self.secret_key, algorithms=[self.algorithm]
            )

            if token_type and decoded_payload.get("token_type") != token_type:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"Token type incorrect: expected '{token_type}' but got '{decoded_payload.get('token_type')}'",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            return decoded_payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token Expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token Invalid",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Decode Error Token: {e}",
            )

    def refresh_token(self, refresh_token_str: str) -> str:
        try:
            payload = self.decode_token(refresh_token_str, token_type="refresh")
        except HTTPException as e:
            raise e

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No sub in Refresh Token",
            )

        new_access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        new_access_token = self.create_access_token(
            data={"sub": user_id, "token_type": "access"},
            expires_delta=new_access_token_expires,
        )
        return new_access_token


jwt_handler = JWTHandler(settings.SECRET_KEY, ALGORITHM)


# def get_jwt_key():
#     logger.debug(len(settings.SECRET_KEY))
#     if len(settings.SECRET_KEY) != 43:
#         logger.error("SECRET_KEY length should be 43")
#         raise Exception("SECRET_KEY length should be 43")

#     k = {"k": settings.SECRET_KEY, "kty": "oct"}
#     jwt_key = jwk.JWK(**k)

#     return jwt_key


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(14)).decode()


# def encode_jwt(payload: dict) -> bytes:
#     try:
#         key = get_jwt_key()
#         Token = jwt.JWT(header=JWT_HEADER, claims=payload)
#         Token.make_signed_token(key)
#         Etoken = jwt.JWT(header=JWE_HEADER, claims=Token.serialize())
#         Etoken.make_encrypted_token(key)
#         encoded_jwt = Etoken.serialize()
#     except Exception:
#         raise AuthError("Couldn't encoding Token")

#     return encoded_jwt


# def decode_jwt(token: str) -> dict:
#     try:
#         key = get_jwt_key()
#         ET = jwt.JWT(key=key, jwt=token, expected_type="JWE")
#         ST = jwt.JWT(key=key, jwt=ET.claims)
#         decoded_token = json.loads(ST.claims)
#         user_token = UserRepository.get_token(decoded_token["id"])
#         if decoded_token["exp"] == user_token.access_token_expires.timestamp():
#             return decoded_token
#         else:
#             return {}

#     except Exception:
#         return {}


# class JWTBearer(HTTPBearer):
#     def __init__(self, auto_error: bool = True):
#         super(JWTBearer, self).__init__(auto_error=auto_error)

#     async def __call__(self, request: Request):
#         credentials: HTTPAuthorizationCredentials = await super(
#             JWTBearer, self
#         ).__call__(request)
#         if credentials:
#             if not credentials.scheme == "Bearer":
#                 raise AuthError(detail="Invalid authentication scheme.")

#             if not self.verify_jwt(credentials.credentials):
#                 raise AuthError(detail="Invalid token or expired token.")
#             return credentials.credentials
#         else:
#             raise AuthError(detail="Invalid authorization code.")

#     def verify_jwt(self, jwt_token: str) -> bool:
#         is_token_valid: bool = False
#         try:
#             payload = decode_jwt(jwt_token)
#         except Exception:
#             payload = None

#         if payload:
#             is_token_valid = True

#         return is_token_valid
