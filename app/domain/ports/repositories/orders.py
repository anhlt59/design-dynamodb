from typing import Any, List, Protocol

from app.domain.models import Order


class IOrderRepository(Protocol):
    def get(self, user_id: str, order_id: str) -> Order:
        ...

    def list(
        self,
        user_id: str,
        filters: dict | None = None,
        limit: int = 50,
        direction: str = "asc",
        cursor: dict | None = None,
    ) -> tuple[List[Order], Any]:
        ...

    def create(self, order: Order):
        ...

    def update(self, user_id: str, order_id: str, attributes: dict):
        ...

    def delete(self, user_id: str, order_id: str):
        ...
