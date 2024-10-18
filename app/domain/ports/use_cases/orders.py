from typing import Protocol

from app.domain.models import Order, PaginatedOutputDTO
from app.domain.models.orders import CreateOrderInputDto, PaginatedOrderInputDto


class IOrderUseCase(Protocol):
    def get(self, user_id: str, order_id: str) -> Order:
        ...

    def list_user_orders(self, user_id: str, dto: PaginatedOrderInputDto) -> PaginatedOutputDTO[Order]:
        ...

    def create(self, user_id: str, dto: CreateOrderInputDto) -> Order:
        ...

    def cancel(self, user_id: str, order_id: str):
        ...
