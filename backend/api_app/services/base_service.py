from typing import Any, Union, Type
from beanie import Document
from bson import ObjectId

from ..repositories import BaseRepository  # Assuming this is also updated for Beanie


class BaseService:
    def __init__(self, repository: BaseRepository):
        self._repository: BaseRepository = repository

    async def get_list(
        self,
        schema: Type[Document] = None,
        **kwargs: Any,
    ) -> list[Document]:
        return await self._repository.get_by_options(schema, **kwargs)

    async def get_by_id(self, id: Union[str, ObjectId]) -> Document:
        return await self._repository.get_by_id(id)

    async def create(
        self,
        schema: Type[Document] = None,
        **kwargs: Any,
    ) -> Document:
        return await self._repository.create(schema, **kwargs)

    async def patch(
        self,
        id: Union[str, ObjectId],
        schema: Type[Document] = None,
        **kwargs: Any,
    ) -> Document:
        return await self._repository.update(id, schema, **kwargs)

    async def patch_attr(
        self,
        id: Union[str, ObjectId],
        attr: str,
        value: Any,
    ) -> Document:
        return await self._repository.update_attr(id, attr, value)

    async def delete_by_id(self, id: Union[str, ObjectId]) -> Document:
        return await self._repository.delete_by_id(id)

    async def disactive_by_id(self, id: Union[str, ObjectId]) -> Document:
        return await self._repository.disactive_by_id(id)
