from typing import TypeVar

from pydantic import BaseModel, ConfigDict, field_validator

from app.utils.encoding import base64_decode_json, base64_encode_json

M = TypeVar("M")


class Response(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True, str_strip_whitespace=True)

    @classmethod
    def jsonify(cls, *args, **kwargs):
        if args:
            return cls.model_validate(*args).model_dump()
        if kwargs:
            return cls(**kwargs).model_dump()


class PageResponse(Response):
    # Attributes
    items: list[M]
    limit: int = 20
    next: str | dict | None = None
    previous: str | dict | None = None

    @field_validator("next", "previous", mode="after")
    @classmethod
    def after_validate_cursor(cls, value):
        return base64_encode_json(value) if isinstance(value, dict) else value


class PageRequest(Response):
    # Attributes
    limit: int = 20
    cursor: str | None = None
    direction: str | None = "asc"

    @field_validator("cursor", mode="after")
    @classmethod
    def after_validate_cursor(cls, value):
        return base64_decode_json(value) if isinstance(value, str) else value
