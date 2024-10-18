from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field, field_validator
from uuid_utils import uuid7

from app.common.utils.datetime_utils import current_utc_timestamp
from app.common.utils.encoding import base64_decode_json, base64_encode_json


class Entity(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True, validate_assignment=True)
    # Attributes
    id: str = Field(default_factory=lambda: str(uuid7()))
    createdAt: int = Field(default_factory=current_utc_timestamp)
    updatedAt: int = Field(default_factory=current_utc_timestamp)


M = TypeVar("M", bound=BaseModel)


class PaginatedInputDTO(BaseModel):
    model_config = ConfigDict(use_enum_values=True, str_strip_whitespace=True)
    # Attributes
    limit: int = 20
    cursor: Any = None
    direction: str = "asc"

    @field_validator("cursor", mode="after")
    @classmethod
    def after_validate_cursor(cls, value):
        if isinstance(value, str):
            return base64_decode_json(value)
        return value


class PaginatedOutputDTO(BaseModel, Generic[M]):
    model_config = ConfigDict(use_enum_values=True, str_strip_whitespace=True)
    # Attributes
    items: list[M]
    limit: int = 20
    next: Any = None
    previous: Any = None

    @field_validator("next", "previous", mode="after")
    @classmethod
    def after_validate_cursor(cls, value):
        if isinstance(value, dict):
            return base64_encode_json(value)
        return value
