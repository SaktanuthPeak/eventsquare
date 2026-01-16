from bson import ObjectId
from bson.errors import InvalidId
import typing as t

from pydantic_core import CoreSchema, core_schema
from pydantic_core.core_schema import ValidationInfo, str_schema
from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler, BaseModel
from pydantic.json_schema import JsonSchemaValue
from pydantic.main import _model_construction

from beanie import Document as BeanieDocument

from api_app.api.core.exceptions import ValidationError

__all__ = ("AllOptional", "PydanticObjectId", "DeDBRef")

T = t.TypeVar("T")


class AllOptional(_model_construction.ModelMetaclass):
    def __new__(self, name, bases, namespaces, **kwargs):
        annotations = namespaces.get("__annotations__", {})
        for base in bases:
            annotations.update(getattr(base, "__annotations__", {}))
        for field in annotations:
            if not field.startswith("__"):
                annotations[field] = t.Optional[annotations[field]]
        namespaces["__annotations__"] = annotations
        return super().__new__(self, name, bases, namespaces, **kwargs)


class PydanticObjectId(ObjectId):
    """
    Object Id field. Compatible with Pydantic.
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, _: ValidationInfo):
        if isinstance(v, bytes):
            v = v.decode("utf-8")
        try:
            return PydanticObjectId(v)
        except InvalidId:
            raise ValueError("Id must be of type PydanticObjectId")

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: t.Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.json_or_python_schema(
            python_schema=core_schema.with_info_plain_validator_function(cls.validate),
            json_schema=str_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: str(instance)
            ),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        schema: core_schema.CoreSchema,
        handler: GetJsonSchemaHandler,
    ) -> JsonSchemaValue:
        json_schema = handler(schema)
        json_schema.update(
            type="string",
            example="60a7b2f65f1b2c6d88f3a2a1",
        )
        return json_schema


class DeDBRef(t.Generic[T]):
    """
    Simulated dereferencing of a document reference for Beanie.

    Use:
    user: DeDBRef[UserModel] = Field(json_schema_extra="user_field")
    """

    def __init__(self, document_class: type[BeanieDocument]):
        self.document_class = document_class

    @classmethod
    def build_validation(cls, handler, source_type):
        async def validate(v, validation_info: core_schema.ValidationInfo):
            document_class: type[BeanieDocument] = t.get_args(source_type)[0]

            if isinstance(v, (dict, BaseModel, ObjectId)):
                return v

            if isinstance(v, str):
                try:
                    return await document_class.get(PydanticObjectId(v))
                except Exception as e:
                    raise ValidationError(f"Invalid reference ID: {e}")

            return v

        return validate

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: t.Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.json_or_python_schema(
            python_schema=core_schema.with_info_plain_validator_function(
                cls.build_validation(handler, source_type)
            ),
            json_schema=core_schema.typed_dict_schema(
                {"ref": core_schema.typed_dict_field(core_schema.str_schema())}
            ),
        )
