from pynamodb.attributes import ListAttribute, MapAttribute, NumberAttribute, UnicodeAttribute
from pynamodb.indexes import AllProjection, GlobalSecondaryIndex

from .base import DynamoMeta, DynamoModel, KeyAttribute


class OrderStatus:
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELED = "CANCELED"
    SHIPPING = "SHIPPING"
    DELIVERED = "DELIVERED"


class GSI1Index(GlobalSecondaryIndex):
    class Meta(DynamoMeta):
        index_name = "gsi1"
        projection = AllProjection()

    gsi1pk = KeyAttribute(hash_key=True, prefix="ORDER#STATUS#")
    gsi1sk = KeyAttribute(range_key=True, prefix="AT#")


class OrderItem(MapAttribute):
    productId = UnicodeAttribute(null=False)
    quantity = NumberAttribute(null=False)
    price = NumberAttribute(null=False)

    def to_dict(self):
        return {
            "productId": self.productId,
            "quantity": self.quantity,
            "price": self.price,
        }


class OrderModel(DynamoModel, discriminator="ORDER"):
    # Keys
    pk = KeyAttribute(hash_key=True, prefix="USER#")
    sk = KeyAttribute(range_key=True, prefix="ORDER#")
    # GSI
    gsi1pk = KeyAttribute(prefix="ORDER#STATUS#", null=False)
    gsi1sk = KeyAttribute(prefix="AT#")
    gsi1 = GSI1Index()
    # Attributes
    userId = UnicodeAttribute(null=False)
    items = ListAttribute(of=OrderItem, null=False)
    totalPrice = NumberAttribute(null=False)
    address = UnicodeAttribute(null=False)
    status = UnicodeAttribute(null=False, default=OrderStatus.PENDING)

    def post_load(self, *args, **kwargs):
        if self.pk is None:
            self.pk = self.userId
        if self.sk is None:
            self.sk = self.id
        if self.gsi1pk is None:
            self.gsi1pk = self.status
        if self.gsi1sk is None:
            self.gsi1sk = self.updatedAt

    def to_dict(self):
        return {
            "id": self.id,
            "userId": self.userId,
            "items": self.items,
            "totalPrice": self.totalPrice,
            "address": self.address,
            "status": self.status,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt,
        }
