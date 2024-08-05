from pydantic import BaseModel as Base
from pydantic import ConfigDict, field_serializer

from app.utils.encode_utils import base64_decode_json, base64_encode_json


class Response(Base):
    id: str | None = None
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    @classmethod
    def jsonify(cls, *args, **kwargs):
        if args:
            return cls.model_validate(*args).model_dump()
        if kwargs:
            return cls(**kwargs).model_dump()


class Page(Response):
    limit: int = 20
    next: str | None = None
    previous: str | None = None


class PageRequest(Response):
    derection: str | None = "asc"
    limit: int = 20
    cursor: str | None = None

    @property
    def parsed_cursor(self) -> dict | None:
        return base64_decode_json(self.cursor)

    @property
    def filters(self) -> dict:
        return {}


class PageResponse(Response):
    items: list
    page: Page
    model_config = ConfigDict(from_attributes=True)

    @field_serializer("page")
    def serialize_page(self, value: Page | None) -> str | None:
        if isinstance(value.next, dict):
            value.next = base64_encode_json(value.next)
        if isinstance(value.previous, dict):
            value.previous = base64_encode_json(value.previous)
        return value

    @classmethod
    def jsonify(
        cls, items: list | None = None, limit: int = 20, next: dict | None = None, previous: dict | None = None
    ) -> dict:
        return cls(items=items, page=Page(limit=limit, next=next, previous=previous)).model_dump()
