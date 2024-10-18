from typing import Any, Protocol

from app.domain.models import Order
from app.domain.models.orders import CreateOrderInputDto, PaginatedOrderInputDto


class IOrderUseCase(Protocol):
    def get(self, user_id: str, order_id: str) -> Order:
        ...

    def list_user_orders(self, user_id: str, dto: PaginatedOrderInputDto) -> tuple[list[Order], Any]:
        ...

    def create(self, user_id: str, dto: CreateOrderInputDto) -> Order:
        ...

    def cancel(self, user_id: str, order_id: str):
        ...
