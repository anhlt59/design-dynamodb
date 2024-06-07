from pynamodb.attributes import UnicodeAttribute
from pynamodb.indexes import AllProjection, GlobalSecondaryIndex

from .base import DynamoMeta, DynamoModel, KeyAttribute


class GSI1Index(GlobalSecondaryIndex):
    class Meta(DynamoMeta):
        index_name = "gsi1"
        projection = AllProjection()

    gsi1pk = KeyAttribute(hash_key=True, default="BRAND")
    gsi1sk = KeyAttribute(range_key=True, prefix="BRAND#NAME#")


class BrandModel(DynamoModel, discriminator="BRAND"):
    # Keys
    pk = KeyAttribute(hash_key=True, default="BRAND")
    sk = KeyAttribute(range_key=True, prefix="BRAND#")
    # GSI
    gsi1pk = KeyAttribute(default="BRAND", null=False)
    gsi1sk = KeyAttribute(prefix="BRAND#NAME#")
    gsi1 = GSI1Index()
    # Attributes
    name = UnicodeAttribute(null=False)

    def post_load(self, *args, **kwargs):
        if self.sk is None:
            self.sk = self.id
        if self.gsi1sk is None:
            self.gsi1sk = self.name

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt,
        }
