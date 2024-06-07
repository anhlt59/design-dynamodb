from pynamodb.attributes import UnicodeAttribute
from pynamodb.indexes import AllProjection, GlobalSecondaryIndex

from .base import DynamoMeta, DynamoModel, KeyAttribute


class GSI1Index(GlobalSecondaryIndex):
    class Meta(DynamoMeta):
        index_name = "gsi1"
        projection = AllProjection()

    gsi1pk = KeyAttribute(hash_key=True, default="USER")
    gsi1sk = KeyAttribute(range_key=True, prefix="EMAIL#")


class UserModel(DynamoModel, discriminator="USER"):
    # Keys
    pk = KeyAttribute(hash_key=True, default="USER")
    sk = KeyAttribute(range_key=True, prefix="USER#")
    # GSI
    gsi1pk = KeyAttribute(default="USER")
    gsi1sk = KeyAttribute(prefix="EMAIL#")
    gsi1 = GSI1Index()
    # Attributes
    name = UnicodeAttribute(null=False)
    email = UnicodeAttribute(null=False)
    password = UnicodeAttribute(null=False)

    def post_load(self, *args, **kwargs):
        if self.sk is None:
            self.sk = self.id
        if self.gsi1sk is None:
            self.gsi1sk = self.email

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt,
        }
