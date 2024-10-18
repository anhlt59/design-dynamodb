from typing import Protocol

from app.domain.models import PaginatedOutputDTO, Product
from app.domain.models.products import CreateProductInputDto, PaginatedProductInputDto, UpdateProductInputDto


class IProductUseCase(Protocol):
    def get(self, id: str) -> Product:
        ...

    def list(self, dto: PaginatedProductInputDto) -> PaginatedOutputDTO[Product]:
        ...

    def create(self, dto: CreateProductInputDto) -> Product:
        ...

    def update(self, id: str, dto: UpdateProductInputDto):
        ...

    def delete(self, id: str):
        ...
