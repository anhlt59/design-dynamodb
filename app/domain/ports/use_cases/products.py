from typing import Any, List, Protocol

from app.domain.models import Product
from app.domain.models.products import CreateProductInputDto, PaginatedProductInputDto, UpdateProductInputDto


class IProductUseCase(Protocol):
    def get(self, id: str) -> Product:
        ...

    def list(self, dto: PaginatedProductInputDto) -> tuple[List[Product], Any]:
        ...

    def create(self, dto: CreateProductInputDto) -> Product:
        ...

    def update(self, id: str, dto: UpdateProductInputDto):
        ...

    def delete(self, id: str):
        ...
