from pynamodb.attributes import UnicodeAttribute
from pynamodb.indexes import AllProjection, GlobalSecondaryIndex

from .base import DynamoMeta, DynamoModel, KeyAttribute


class GSI1Index(GlobalSecondaryIndex):
    class Meta(DynamoMeta):
        index_name = "gsi1"
        projection = AllProjection()

    gsi1pk = KeyAttribute(hash_key=True, default="CAT")
    gsi1sk = KeyAttribute(range_key=True, prefix="CAT#NAME#")


class CategoryModel(DynamoModel, discriminator="CATEGORY"):
    # Keys
    pk = KeyAttribute(hash_key=True, default="CAT")
    sk = KeyAttribute(range_key=True, prefix="CAT#")
    # GSI
    gsi1pk = KeyAttribute(default="CAT", null=False)
    gsi1sk = KeyAttribute(prefix="CAT#NAME#")
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
