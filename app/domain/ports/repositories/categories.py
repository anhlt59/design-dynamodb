from typing import Protocol

from pynamodb.transactions import Transaction

from app.domain.models import Category, PaginatedOutputDTO


class ICategoryRepository(Protocol):
    def set_transaction(self, transaction: Transaction):
        ...

    def get(self, id: str) -> Category:
        ...

    def list(
        self, limit: int = 50, direction: str = "asc", cursor: dict | None = None
    ) -> PaginatedOutputDTO[Category]:
        ...

    def list_by_name(
        self, name: str, limit: int = 50, direction: str = "asc", cursor: dict | None = None
    ) -> PaginatedOutputDTO[Category]:
        ...

    def create(self, category: Category):
        ...

    def update(self, id: str, attributes: dict):
        ...

    def delete(self, id: str):
        ...

    def count_by_name(self, name: str):
        ...
