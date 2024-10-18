from typing import Any, List, Protocol

from app.domain.models import Brand
from app.domain.models.brands import CreateBrandInputDto, PaginatedBrandInputDto, UpdateBrandInputDto


class IBrandUseCase(Protocol):
    def get(self, id: str) -> Brand:
        ...

    def list(self, dto: PaginatedBrandInputDto) -> tuple[List[Brand], Any]:
        ...

    def create(self, dto: CreateBrandInputDto) -> Brand:
        ...

    def update(self, id: str, dto: UpdateBrandInputDto):
        ...

    def delete(self, id: str):
        ...
