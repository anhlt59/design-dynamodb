from typing import Protocol

from app.domain.models import Brand, PaginatedOutputDTO
from app.domain.models.brands import CreateBrandInputDto, PaginatedBrandInputDto, UpdateBrandInputDto


class IBrandUseCase(Protocol):
    def get(self, id: str) -> Brand:
        ...

    def list(self, dto: PaginatedBrandInputDto) -> PaginatedOutputDTO[Brand]:
        ...

    def create(self, dto: CreateBrandInputDto) -> Brand:
        ...

    def update(self, id: str, dto: UpdateBrandInputDto):
        ...

    def delete(self, id: str):
        ...
