from typing import Any, List, Protocol

from app.domain.models import Category


class ICategoryRepository(Protocol):
    def get(self, id: str) -> Category:
        ...

    def list(self, limit: int = 50, direction: str = "asc", cursor: dict | None = None) -> tuple[List[Category], Any]:
        ...

    def list_by_name(
        self, name: str, limit: int = 50, direction: str = "asc", cursor: dict | None = None
    ) -> tuple[List[Category], Any]:
        ...

    def create(self, category: Category):
        ...

    def update(self, id: str, attributes: dict):
        ...

    def delete(self, id: str):
        ...

    def count_by_name(self, name: str):
        ...
