import typing as t

from pydantic import BaseModel

from bson import ObjectId

from mongoengine import Document, QuerySet, EmbeddedDocument

from ..repositories import BaseRepository


class BaseService:
    def __init__(self, repository: BaseRepository):
        self._repository: BaseRepository = repository

    def get_list(
        self,
        schema: BaseModel | None = None,
        **kwargs: t.Any,
    ) -> QuerySet:
        return self._repository.get_by_options(schema, **kwargs)

    def get_by_id(self, id: str | ObjectId) -> Document:
        return self._repository.get_by_id(id)

    def create(
        self,
        schema: BaseModel | None = None,
        **kwargs: t.Any,
    ) -> Document:
        return self._repository.create(schema, **kwargs)

    def patch(
        self,
        id: str | ObjectId,
        schema: BaseModel | None = None,
        **kwargs: t.Any,
    ) -> Document:
        return self._repository.update(id, schema, **kwargs)

    def patch_attr(self, id: str | ObjectId, attr: str, value: t.Any) -> Document:
        return self._repository.update_attr(id, attr, value)

    def delete_by_id(self, id: str | ObjectId) -> Document:
        return self._repository.delete_by_id(id)

    def disactive_by_id(self, id: str | ObjectId) -> Document:
        return self._repository.disactive_by_id(id)

    def update_request_logs(
        self,
        id: str | ObjectId,
        request_log: EmbeddedDocument,
    ) -> Document:
        return self._repository.update_request_logs(id, request_log)
