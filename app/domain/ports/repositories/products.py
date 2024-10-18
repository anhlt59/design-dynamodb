from typing import Protocol

from pynamodb.transactions import Transaction

from app.domain.models import PaginatedOutputDTO, Product


class IProductRepository(Protocol):
    def set_transaction(self, transaction: Transaction):
        ...

    def get(self, id: str) -> Product:
        ...

    def list(
        self, filters: dict | None = None, direction: str = "asc", cursor: dict | None = None, limit: int = 50
    ) -> PaginatedOutputDTO[Product]:
        ...

    def list_by_brand(
        self,
        brand_id: str,
        filters: dict | None = None,
        direction: str = "asc",
        cursor: dict | None = None,
        limit: int = 50,
    ) -> PaginatedOutputDTO[Product]:
        ...

    def list_by_category(
        self,
        category_id: str,
        filters: dict | None = None,
        direction: str = "asc",
        cursor: dict | None = None,
        limit: int = 50,
    ) -> PaginatedOutputDTO[Product]:
        ...

    def create(self, product: Product):
        ...

    def decrease_stock(self, id: str, quantity: int):
        ...

    def update(self, id: str, attributes: dict):
        ...

    def delete(self, id: str):
        ...
