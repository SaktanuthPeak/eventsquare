import re
import typing as t
import datetime
from calendar import timegm
from bson import ObjectId
from mongoengine import Document, errors

from ..models import User, Token
from ..repositories.base_repo import BaseRepository
from ..api.core.exceptions import DuplicatedError, ValidationError

from loguru import logger


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    def get_unique_username(self, username: str) -> Document | None:
        try:
            item = self.model.objects(username=username).first()
        except Exception:
            raise ValidationError(detail="Invalid username")

        return item

    @staticmethod
    def get_token_by_id(id: str | ObjectId) -> Token:
        item = Token.objects.with_id(id)
        if not Token:
            raise ValidationError(detail="Token not found")
        return item

    @staticmethod
    def get_token(owner: str | User) -> Token | None:
        if isinstance(owner, (str, ObjectId)):
            owner = UserRepository().get_by_id(owner)

        item = Token.objects(owner=owner).first()
        return item

    @staticmethod
    def update_token(owner: User, tokens: dict[str, t.Any]) -> Token:
        item = UserRepository.get_token(owner)
        if not item:
            raise ValidationError(detail="Token not found")

        item.update(**tokens)

        return UserRepository.get_token_by_id(item.id)

    @staticmethod
    def create_token(user: User, tokens: dict[str, t.Any]) -> Token:
        try:
            item = Token(owner=user, **tokens)
            item.save()
        except errors.NotUniqueError as e:
            duplicate = re.search("'keyValue': {.*?}", str(e)).group(0)
            duplicate = re.search("{.*?}", duplicate).group(0)
            raise DuplicatedError(detail=f"'DuplicateError': {duplicate}")

        except Exception:
            raise ValidationError(detail="Cannot create Token")

        return UserRepository.get_token_by_id(item.id)

    @staticmethod
    def create_or_update_token(owner: User, tokens: dict[str, t.Any]) -> Token:
        item = UserRepository.get_token(owner)
        if not item:
            item = Token(
                owner=owner,
                access_token=tokens["access_token"],
                refresh_token=tokens["refresh_token"],
                access_token_expires=datetime.datetime.fromtimestamp(
                    timegm(tokens["access_token_expires"].timetuple())
                ),
                refresh_token_expires=datetime.datetime.fromtimestamp(
                    timegm(tokens["refresh_token_expires"].timetuple())
                ),
            )
            try:
                item.save()

            except errors.NotUniqueError as e:
                duplicate = re.search("'keyValue': {.*?}", str(e)).group(0)
                duplicate = re.search("{.*?}", duplicate).group(0)
                raise DuplicatedError(f"'DuplicateError': {duplicate}")

            except Exception as e:
                print(e)
                raise ValidationError("Cannot create Token")
        else:
            item.update(
                access_token=tokens["access_token"],
                refresh_token=tokens["refresh_token"],
                access_token_expires=datetime.datetime.fromtimestamp(
                    timegm(tokens["access_token_expires"].timetuple())
                ),
                refresh_token_expires=datetime.datetime.fromtimestamp(
                    timegm(tokens["refresh_token_expires"].timetuple())
                ),
            )

        return UserRepository.get_token_by_id(item.id)
