import re
import datetime
import typing as t

from pydantic import BaseModel

from bson import ObjectId

from mongoengine import Document, QuerySet, EmbeddedDocument
from mongoengine.errors import NotUniqueError

from ..api.core.exceptions import DuplicatedError, ValidationError


class BaseRepository:
    def __init__(self, model: Document):
        self.model = model

    def get_by_options(
        self,
        schema: BaseModel | None = None,
        exclude_defaults: bool = True,
        exclude_none: bool = False,
        exclude_unset: bool = True,
        **kwargs: t.Any,
    ) -> QuerySet:
        if "query" in kwargs:
            query = kwargs.pop("query")
            items = self.model.objects(
                query,
                **self.dump_schema(
                    schema, exclude_defaults, exclude_none, exclude_unset, **kwargs
                ),
            )
        else:
            items = self.model.objects(
                **self.dump_schema(
                    schema, exclude_defaults, exclude_none, exclude_unset, **kwargs
                )
            )

        # if not items:
        #     raise NotFoundError(detail="Data not found")

        return items

    def get_by_id(self, id: str | ObjectId) -> Document:
        if not ObjectId.is_valid(id):
            raise ValidationError("Invalid ObjectId")

        item = self.model.objects.with_id(id)
        # if not item:
        #     raise NotFoundError(detail=f"ObjectId('{str(id)}') not found")

        return item

    def create(
        self,
        schema: None | BaseModel = None,
        exclude_defaults: bool = True,
        exclude_none: bool = False,
        exclude_unset: bool = True,
        **kwargs: t.Any,
    ) -> Document:
        request_log = None
        if "request_log" in kwargs:
            request_log = kwargs.pop("request_log")
            if isinstance(request_log, list) and len(request_log) != 0:
                request_log = request_log.pop()

        try:
            item = self.model(
                **self.dump_schema(
                    schema, exclude_defaults, exclude_none, exclude_unset, **kwargs
                )
            )
            item.save()
            if request_log:
                self.update_request_logs(item.id, request_log)

        except NotUniqueError as e:
            duplicate = re.search("'keyValue': {.*?}", str(e)).group(0)
            duplicate = re.search("{.*?}", duplicate).group(0)
            raise DuplicatedError(f"'DuplicateError': {duplicate}")

        except Exception as e:
            raise ValidationError(str(e))

        return self.get_by_id(item.id)

    def update(
        self,
        id: str | ObjectId,
        schema: BaseModel | None = None,
        exclude_defaults: bool = True,
        exclude_none: bool = False,
        exclude_unset: bool = True,
        **kwargs: t.Any,
    ) -> Document:
        item = self.get_by_id(id)
        if hasattr(item, "updated_date"):
            kwargs["updated_date"] = datetime.datetime.now()

        request_log = None
        if "request_log" in kwargs:
            request_log = kwargs.pop("request_log")

        try:
            item.update(
                **self.dump_schema(
                    schema, exclude_defaults, exclude_none, exclude_unset, **kwargs
                )
            )
        except Exception as e:
            raise ValidationError(detail=str(e))

        if request_log:
            self.update_request_logs(item.id, request_log)

        return self.get_by_id(item.id)

    def update_attr(
        self,
        id: str | ObjectId,
        attr: str,
        value: t.Any,
        request_log: EmbeddedDocument = None,
    ) -> Document:
        return self.update(id, **{attr: value}, request_log=request_log)

    def delete_by_id(self, id: str | ObjectId) -> Document:
        item = self.get_by_id(id)
        try:
            item.delete()
        except Exception as e:
            raise ValidationError(detail=str(e))

        return item

    def disactive_by_id(
        self, id: str | ObjectId, request_log: EmbeddedDocument = None
    ) -> Document:
        item = self.get_by_id(id)
        if hasattr(item, "status"):
            return self.update_attr(item.id, "status", "disactive", request_log)
        else:
            raise ValidationError(detail="Document has no attribute status")

    def update_request_logs(
        self,
        id: str | ObjectId,
        request_log: EmbeddedDocument,
    ) -> None:
        item = self.get_by_id(id)
        if hasattr(item, "request_logs"):
            try:
                item.request_logs.create(**request_log.to_mongo())
                item.save()
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
    ) -> dict[str]:
        """Merge schema and kwargs.

        If schema have same attributes with kwargs,
        those attributes in schema will have replaced by kwargs's attributes value.
        """

        schema_dict = (
            schema.model_dump(
                exclude_unset=exclude_unset,
                exclude_none=exclude_none,
                exclude_defaults=exclude_defaults,
            )
            if schema
            else {}
        )

        return {
            k: v for d in [schema_dict, kwargs] for k, v in d.items()
        }  # Merge schema and kwargs
