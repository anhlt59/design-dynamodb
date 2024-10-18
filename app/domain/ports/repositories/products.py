from typing import Any, List, Protocol

from app.domain.models import Product


class IProductRepository(Protocol):
    def get(self, id: str) -> Product:
        ...

    def list(
        self, filters: dict | None = None, direction: str = "asc", cursor: dict | None = None, limit: int = 50
    ) -> tuple[List[Product], Any]:
        ...

    def list_by_brand(
        self,
        brand_id: str,
        filters: dict | None = None,
        direction: str = "asc",
        cursor: dict | None = None,
        limit: int = 50,
    ) -> tuple[List[Product], Any]:
        ...

    def list_by_category(
        self,
        category_id: str,
        filters: dict | None = None,
        direction: str = "asc",
        cursor: dict | None = None,
        limit: int = 50,
    ) -> tuple[List[Product], Any]:
        ...

    def create(self, product: Product):
        ...

    def decrease_stock(self, id: str, quantity: int):
        ...

    def update(self, id: str, attributes: dict):
        ...

    def delete(self, id: str):
        ...
