from pynamodb.attributes import UnicodeAttribute
from pynamodb.indexes import AllProjection, LocalSecondaryIndex

from .base import DynamoMeta, DynamoModel, KeyAttribute


class LSIIndex(LocalSecondaryIndex):
    class Meta(DynamoMeta):
        index_name = "lsi"
        projection = AllProjection()

    pk = KeyAttribute(hash_key=True, default="BRAND")
    sku = KeyAttribute(range_key=True, prefix="BRAND#NAME#")


class BrandModel(DynamoModel, discriminator="BRAND"):  # type: ignore
    # Keys
    pk = KeyAttribute(hash_key=True, default="BRAND")
    sk = KeyAttribute(range_key=True, prefix="BRAND#")
    # Index
    sku = KeyAttribute(prefix="BRAND#NAME#")
    lsi = LSIIndex()
    # Attributes
    name = UnicodeAttribute(null=False)

    def post_load(self, *args, **kwargs):
        if self.sk is None:
            self.sk = self.id
        if self.sku is None:
            self.sku = self.name
