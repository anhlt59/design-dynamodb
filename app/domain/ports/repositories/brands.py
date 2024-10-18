from typing import Protocol

from pynamodb.transactions import Transaction

from app.domain.models import Brand, PaginatedOutputDTO


class IBrandRepository(Protocol):
    def set_transaction(self, transaction: Transaction):
        ...

    def get(self, id: str) -> Brand:
        ...

    def list(self, limit: int = 50, direction: str = "asc", cursor: dict | None = None) -> PaginatedOutputDTO[Brand]:
        ...

    def list_by_name(
        self, name: str, limit: int = 50, direction: str = "asc", cursor: dict | None = None
    ) -> PaginatedOutputDTO[Brand]:
        ...

    def create(self, brand: Brand):
        ...

    def update(self, id: str, attributes: dict):
        ...

    def delete(self, id: str):
        ...

    def count_by_name(self, name: str):
        ...
