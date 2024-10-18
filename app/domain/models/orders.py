from pydantic import BaseModel, ConfigDict

from app.common.enums import OrderStatus

from .base import Entity, PaginatedInputDTO


class OrderItem(Entity):
    productId: str
    quantity: int
    price: float


class Order(Entity):
    userId: str
    items: list[OrderItem]
    address: str
    status: OrderStatus = OrderStatus.PENDING


# DTOs -----------------------------------------------------
class CreateOrderInputDto(BaseModel):
    address: str
    items: list[OrderItem]


class OrderOutputDto(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    # Attributes
    id: str
    userId: str
    items: list[OrderItem]
    address: str
    status: OrderStatus
    createdAt: int
    updatedAt: int


class PaginatedOrderInputDto(PaginatedInputDTO):
    status: OrderStatus | None = None
    since: int | None = None
    until: int | None = None
