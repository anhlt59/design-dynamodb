from pynamodb.attributes import NumberAttribute, UnicodeAttribute
from pynamodb.indexes import AllProjection, GlobalSecondaryIndex

from .base import DynamoMeta, DynamoModel, IntegerAttribute, KeyAttribute


class GSI1Index(GlobalSecondaryIndex):
    class Meta(DynamoMeta):
        index_name = "gsi1"
        projection = AllProjection()

    gsi1pk = KeyAttribute(hash_key=True, prefix="BRAND#")
    gsi1sk = KeyAttribute(range_key=True, prefix="CAT#")


class GSI2Index(GlobalSecondaryIndex):
    class Meta(DynamoMeta):
        index_name = "gsi2"
        projection = AllProjection()

    gsi2pk = KeyAttribute(hash_key=True, prefix="CAT#")
    gsi2sk = KeyAttribute(range_key=True, prefix="BRAND#")


class ProductModel(DynamoModel, discriminator="PRODUCT"):  # type: ignore
    # Keys
    pk = KeyAttribute(default="PROD", hash_key=True)
    sk = KeyAttribute(prefix="PROD#", range_key=True)
    # Index
    gsi1pk = KeyAttribute(prefix="BRAND#")
    gsi1sk = KeyAttribute(prefix="CAT#")
    gsi1 = GSI1Index()
    gsi2pk = KeyAttribute(prefix="CAT#")
    gsi2sk = KeyAttribute(prefix="BRAND#")
    gsi2 = GSI2Index()
    # Attributes
    name = UnicodeAttribute(null=False)
    price = NumberAttribute(null=False)
    stock = IntegerAttribute(null=False)
    categoryId = UnicodeAttribute(null=False)
    brandId = UnicodeAttribute(null=True)

    def post_load(self, *args, **kwargs):
        if self.sk is None:
            self.sk = self.id
        if self.gsi1pk is None:
            self.gsi1pk = self.brandId
        if self.gsi1sk is None:
            self.gsi1sk = f"{self.categoryId}#AT#{self.createdAt}"
        if self.gsi2pk is None:
            self.gsi2pk = self.categoryId
        if self.gsi2sk is None:
            self.gsi2sk = f"{self.brandId}#AT#{self.createdAt}"
