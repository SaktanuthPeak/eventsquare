import re
import datetime
import typing as t
from bson import ObjectId
from pydantic import BaseModel
from beanie import Document
from ..utils.schema import PydanticObjectId

from api_app.api.core.exceptions import DuplicatedError, ValidationError


class BaseRepository:
    def __init__(self, model: t.Type[Document]):
        self.model = model

    async def get_by_options(
        self,
        schema: BaseModel | None = None,
        exclude_defaults: bool = True,
        exclude_none: bool = False,
        exclude_unset: bool = True,
        **kwargs: t.Any,
    ) -> list[Document]:
        query_dict = self.dump_schema(
            schema, exclude_defaults, exclude_none, exclude_unset, **kwargs
        )
        cursor = self.model.find(query_dict)
        return await cursor.to_list()

    async def get_by_id(self, id: str | ObjectId) -> Document:
        if not ObjectId.is_valid(id):
            raise ValidationError("Invalid ObjectId")

        item = await self.model.get(PydanticObjectId(id))
        if not item:
            raise ValidationError(f"ObjectId('{id}') not found")
        return item

    async def create(
        self,
        schema: BaseModel | None = None,
        exclude_defaults: bool = True,
        exclude_none: bool = False,
        exclude_unset: bool = True,
        **kwargs: t.Any,
    ) -> Document:
        request_log = kwargs.pop("request_log", None)
        if isinstance(request_log, list) and len(request_log) != 0:
            request_log = request_log.pop()

        try:
            data = self.dump_schema(
                schema, exclude_defaults, exclude_none, exclude_unset, **kwargs
            )
            item = self.model(**data)
            await item.insert()

            if request_log:
                await self.update_request_logs(item.id, request_log)

        except Exception as e:
            if "E11000" in str(e):  # MongoDB duplicate error
                duplicate = re.search("'keyValue': {.*?}", str(e))
                if duplicate:
                    duplicate = re.search("{.*?}", duplicate.group(0)).group(0)
                raise DuplicatedError(f"'DuplicateError': {duplicate}")
            raise ValidationError(str(e))

        return await self.get_by_id(item.id)

    async def update(
        self,
        id: str | ObjectId,
        schema: BaseModel | None = None,
        exclude_defaults: bool = True,
        exclude_none: bool = False,
        exclude_unset: bool = True,
        **kwargs: t.Any,
    ) -> Document:
        item = await self.get_by_id(id)
        if hasattr(item, "updated_date"):
            kwargs["updated_date"] = datetime.datetime.utcnow()

        request_log = kwargs.pop("request_log", None)

        try:
            update_data = self.dump_schema(
                schema, exclude_defaults, exclude_none, exclude_unset, **kwargs
            )
            await item.set(update_data)
        except Exception as e:
            raise ValidationError(detail=str(e))

        if request_log:
            await self.update_request_logs(item.id, request_log)

        return await self.get_by_id(item.id)

    async def update_attr(
        self,
        id: str | ObjectId,
        attr: str,
        value: t.Any,
        request_log: BaseModel = None,
    ) -> Document:
        return await self.update(id, **{attr: value}, request_log=request_log)

    async def delete_by_id(self, id: str | ObjectId) -> Document:
        item = await self.get_by_id(id)
        try:
            await item.delete()
        except Exception as e:
            raise ValidationError(detail=str(e))

        return item

    async def disactive_by_id(
        self, id: str | ObjectId, request_log: BaseModel = None
    ) -> Document:
        item = await self.get_by_id(id)
        if hasattr(item, "status"):
            return await self.update_attr(item.id, "status", "disactive", request_log)
        else:
            raise ValidationError(detail="Document has no attribute status")

    async def update_request_logs(
        self,
        id: str | ObjectId,
        request_log: BaseModel,
    ) -> None:
        item = await self.get_by_id(id)
        if hasattr(item, "request_logs"):
            try:
                item.request_logs.append(request_log.model_dump())
                await item.save()
            except Exception as e:
                raise ValidationError(str(e))
        else:
            raise ValidationError("Document has no attribute request_logs")

    def dump_schema(
        self,
        schema: BaseModel | None = None,
        exclude_defaults: bool = True,
        exclude_none: bool = False,
        exclude_unset: bool = True,
        **kwargs: t.Any,
    ) -> dict[str, t.Any]:
        schema_dict = (
            schema.model_dump(
                exclude_unset=exclude_unset,
                exclude_none=exclude_none,
                exclude_defaults=exclude_defaults,
            )
            if schema
            else {}
        )
        return {k: v for d in [schema_dict, kwargs] for k, v in d.items()}
