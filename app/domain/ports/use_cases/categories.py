from typing import Protocol

from app.domain.models import Category, PaginatedOutputDTO
from app.domain.models.categories import CreateCategoryInputDto, PaginatedCategoryInputDto, UpdateCategoryInputDto


class ICategoryUseCase(Protocol):
    def get(self, id: str) -> Category:
        ...

    def list(self, dto: PaginatedCategoryInputDto) -> PaginatedOutputDTO[Category]:
        ...

    def create(self, dto: CreateCategoryInputDto) -> Category:
        ...

    def update(self, id: str, dto: UpdateCategoryInputDto):
        ...

    def delete(self, id: str):
        ...
