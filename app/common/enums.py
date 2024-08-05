from enum import Enum


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELED = "CANCELED"
    SHIPPING = "SHIPPING"
    DELIVERED = "DELIVERED"
