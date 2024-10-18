from typing import Protocol

from pynamodb.transactions import Transaction

from app.domain.models import Order, PaginatedOutputDTO


class IOrderRepository(Protocol):
    def set_transaction(self, transaction: Transaction):
        ...

    def get(self, user_id: str, order_id: str) -> Order:
        ...

    def list(
        self,
        user_id: str,
        filters: dict | None = None,
        direction: str = "asc",
        cursor: dict | None = None,
        limit: int = 50,
    ) -> PaginatedOutputDTO[Order]:
        ...

    def create(self, order: Order):
        ...

    def update(self, user_id: str, order_id: str, attributes: dict):
        ...

    def delete(self, user_id: str, order_id: str):
        ...
