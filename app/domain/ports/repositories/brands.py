from typing import Any, List, Protocol

from app.domain.models import Brand


class IBrandRepository(Protocol):
    def get(self, id: str) -> Brand:
        ...

    def list(self, limit: int = 50, direction: str = "asc", cursor: dict | None = None) -> tuple[List[Brand], Any]:
        ...

    def list_by_name(
        self, name: str, limit: int = 50, direction: str = "asc", cursor: dict | None = None
    ) -> tuple[List[Brand], Any]:
        ...

    def create(self, brand: Brand):
        ...

    def update(self, id: str, attributes: dict):
        ...

    def delete(self, id: str):
        ...

    def count_by_name(self, name: str):
        ...
