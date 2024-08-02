from enum import Enum

from .base import BaseEntity


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELED = "CANCELED"
    SHIPPING = "SHIPPING"
    DELIVERED = "DELIVERED"


class OrderItem(BaseEntity):
    productId: str
    quantity: int
    price: float


class OrderEntity(BaseEntity):
    userId: str
    items: list[OrderItem]
    totalPrice: float
    address: str
    status: OrderStatus
    createdAt: int
    updatedAt: int
