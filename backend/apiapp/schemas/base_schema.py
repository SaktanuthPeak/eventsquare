from pydantic import BaseModel, Field, ConfigDict

from ..utils.schema import PydanticObjectId


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,  # from orm_mode
        validate_default=True,
    )


class BaseSchemaExtra(BaseSchema):
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,  # from orm_mode
        validate_default=True,
        extra="allow",
    )


class BaseSchemaId(BaseSchema):
    id: PydanticObjectId = Field(
        alias="_id", serialization_alias="id"
    )  # serialization_alias made not require response_model_by_alias=False in api router


class FindBase(BaseSchema): ...


class SearchOptions(FindBase): ...


class FindResult(BaseSchema): ...


class FindDateRange(BaseSchema): ...
