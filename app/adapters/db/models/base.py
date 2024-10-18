import json
from typing import Any

from pynamodb.attributes import Attribute, DiscriminatorAttribute, UnicodeAttribute
from pynamodb.models import Model
from pynamodb.types import NUMBER
from uuid_utils import uuid7

from app.common.configs import DYNAMODB_ENDPOINT, DYNAMODB_REGION, DYNAMODB_TABLE_NAME
from app.common.utils.datetime_utils import current_utc_timestamp


# Attributes -----------------------------------------------------------
class KeyAttribute(UnicodeAttribute):
    prefix: str | None

    def __init__(self, prefix: str | None = None, **kwargs):
        super().__init__(**kwargs)
        self.prefix = prefix

    def serialize(self, value: str) -> str:
        if self.prefix is not None:
            value = f"{self.prefix}{value}"
        return super().serialize(value)

    def deserialize(self, value: str) -> str:
        if "#" in value:
            value = value.rsplit("#", 1)[-1]
        return super().deserialize(value)

    def __set__(self, instance: Any, value: Any) -> None:
        if isinstance(value, str) and self.prefix and value.startswith(self.prefix):
            value = value.strip(self.prefix)
        return super().__set__(instance, value)


class IntegerAttribute(Attribute[int]):
    attr_type = NUMBER

    def serialize(self, value):
        return int(value)

    def deserialize(self, value):
        return json.loads(value)


# Model --------------------------------------------------------------
class DynamoMeta:
    table_name: str = DYNAMODB_TABLE_NAME
    host: str | None = DYNAMODB_ENDPOINT
    region: str | None = DYNAMODB_REGION
    read_timeout_seconds: int = 10
    connect_timeout_seconds: int = 10


class DynamoModel(Model):
    Meta = DynamoMeta  # type: ignore
    # Keys
    pk = UnicodeAttribute(hash_key=True)
    sk = UnicodeAttribute(range_key=True)
    # Attributes
    id = UnicodeAttribute(null=False, default_for_new=lambda: str(uuid7()))
    createdAt = IntegerAttribute(default_for_new=current_utc_timestamp)
    updatedAt = IntegerAttribute(default=current_utc_timestamp)
    type = DiscriminatorAttribute()

    def __init__(self, *args: Any, **kwargs: Any):
        self.pre_load(*args, **kwargs)
        super().__init__(*args, **kwargs)
        self.post_load(*args, **kwargs)

    def pre_load(self, *args, **kwargs):
        ...

    def post_load(self, *args, **kwargs):
        ...

    def to_dict(self) -> dict:
        return self.to_simple_dict()
