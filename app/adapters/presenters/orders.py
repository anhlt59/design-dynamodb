from app.common.enums import OrderStatus

from .base import PageRequest, PageResponse, Response


class OrderItem(Response):
    productId: str
    quantity: int
    price: float


class OrderCreateRequest(Response):
    address: str
    items: list[OrderItem]


class OrderResponse(Response):
    id: str
    userId: str
    items: list[OrderItem]
    totalPrice: float
    address: str
    status: OrderStatus
    createdAt: int
    updatedAt: int


class OrdersRequest(PageRequest):
    status: OrderStatus | None = None
    since: int | None = None
    until: int | None = None


class OrdersResponse(PageResponse):
    items: list[OrderResponse]
