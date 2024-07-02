from pynamodb.attributes import UnicodeAttribute
from pynamodb.indexes import AllProjection, LocalSecondaryIndex

from .base import DynamoMeta, DynamoModel, KeyAttribute


class LSIIndex(LocalSecondaryIndex):
    class Meta(DynamoMeta):
        index_name = "lsi"
        projection = AllProjection()

    pk = KeyAttribute(hash_key=True, default="CAT")
    sku = KeyAttribute(range_key=True, prefix="CAT#NAME#")


class CategoryModel(DynamoModel, discriminator="CATEGORY"):
    # Keys
    pk = KeyAttribute(hash_key=True, default="CAT")
    sk = KeyAttribute(range_key=True, prefix="CAT#")
    # GSI
    sku = KeyAttribute(prefix="CAT#NAME#")
    lsi = LSIIndex()
    # Attributes
    name = UnicodeAttribute(null=False)

    def post_load(self, *args, **kwargs):
        if self.sk is None:
            self.sk = self.id
        if self.sku is None:
            self.sku = self.name

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt,
        }
