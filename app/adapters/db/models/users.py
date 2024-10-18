from pynamodb.attributes import UnicodeAttribute
from pynamodb.indexes import AllProjection, LocalSecondaryIndex

from .base import DynamoMeta, DynamoModel, KeyAttribute


class LSIIndex(LocalSecondaryIndex):
    class Meta(DynamoMeta):
        index_name = "lsi"
        projection = AllProjection()

    pk = KeyAttribute(hash_key=True, default="USER")
    sku = KeyAttribute(range_key=True, prefix="EMAIL#")


class UserModel(DynamoModel, discriminator="USER"):  # type: ignore
    # Keys
    pk = KeyAttribute(hash_key=True, default="USER")
    sk = KeyAttribute(range_key=True, prefix="USER#")
    # Index
    sku = KeyAttribute(prefix="EMAIL#")
    lsi = LSIIndex()
    # Attributes
    name = UnicodeAttribute(null=False)
    email = UnicodeAttribute(null=False)
    password = UnicodeAttribute(null=False)

    def post_load(self, *args, **kwargs):
        if self.sk is None:
            self.sk = self.id
        if self.sku is None:
            self.sku = self.email
