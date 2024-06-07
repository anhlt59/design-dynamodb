from dataclasses import dataclass
from typing import Any

from ksuid import ksuid
from pynamodb.attributes import DiscriminatorAttribute, NumberAttribute, UnicodeAttribute
from pynamodb.indexes import Projection
from pynamodb.models import Model

from src.config import AWS_ENDPOINT, AWS_REGION, DYNAMODB_TABLE_NAME
from src.utils.datetime_utils import current_utc_timestamp


# Attributes -----------------------------------------------------------
class KeyAttribute(UnicodeAttribute):
    prefix: str

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


# Model --------------------------------------------------------------
@dataclass
class DynamoMeta:
    table_name: str = DYNAMODB_TABLE_NAME
    host: str | None = AWS_ENDPOINT
    region: str | None = AWS_REGION
    read_timeout_seconds: int = 10
    index_name: str | None = None
    projection: Projection | None = None


class DynamoModel(Model):
    __slots__ = ()
    Meta = DynamoMeta
    # Keys
    pk = UnicodeAttribute(hash_key=True)
    sk = UnicodeAttribute(range_key=True)
    # Attributes
    id = UnicodeAttribute(null=False, default_for_new=lambda: str(ksuid()))
    createdAt = NumberAttribute(default_for_new=current_utc_timestamp)
    updatedAt = NumberAttribute(default=current_utc_timestamp)
    type = DiscriminatorAttribute()

    def __init__(self, *args: Any, **kwargs: Any):
        self.pre_load(*args, **kwargs)
        super().__init__(*args, **kwargs)
        self.post_load(*args, **kwargs)

    def pre_load(self, *args, **kwargs):
        pass

    def post_load(self, *args, **kwargs):
        pass

    def to_dict(self) -> dict:
        return self.to_simple_dict()
