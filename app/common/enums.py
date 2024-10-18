from enum import Enum


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    SHIPPING = "SHIPPING"
    DELIVERED = "DELIVERED"
