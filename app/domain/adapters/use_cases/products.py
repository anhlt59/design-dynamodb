from app.common.exceptions.http import NotFoundException
from app.domain.models import (
    CreateProductInputDto,
    PaginatedOutputDTO,
    PaginatedProductInputDto,
    Product,
    UpdateProductInputDto,
)
from app.domain.ports.unit_of_works import IProductUnitOfWork


class ProductUseCase:
    def __init__(self, uow: IProductUnitOfWork):
        self.uow = uow

    def get(self, id: str) -> Product:
        with self.uow:
            if product := self.uow.products.get(id):
                return product
            raise NotFoundException(f"Product<id={id}> not found")

    def create(self, dto: CreateProductInputDto) -> Product:
        product = Product.model_validate(dto)
        with self.uow:
            if self.uow.categories.get(product.categoryId) is None:
                raise NotFoundException(f"Category<{product.categoryId}> not found")
            if self.uow.brands.get(product.brandId) is None:
                raise NotFoundException(f"Brand<{product.brandId}> not found")

            self.uow.products.create(product)
            self.uow.commit()
            return product

    def update(self, id: str, dto: UpdateProductInputDto):
        if attributes := dto.model_dump(exclude_none=True):
            with self.uow:
                self.uow.products.update(id, attributes)
                self.uow.commit()

    def delete(self, id: str):
        with self.uow:
            self.uow.products.delete(id)
            self.uow.commit()

    def list(self, dto: PaginatedProductInputDto) -> PaginatedOutputDTO[Product]:
        filters = dto.model_dump(exclude_none=True, exclude={"limit", "direction", "cursor"})
        with self.uow:
            if dto.brandId:
                return self.uow.products.list_by_brand(
                    dto.brandId,
                    filters=filters,
                    limit=dto.limit,
                    direction=dto.direction,
                    cursor=dto.cursor,
                )
            if dto.categoryId:
                return self.uow.products.list_by_category(
                    dto.categoryId,
                    filters=filters,
                    limit=dto.limit,
                    direction=dto.direction,
                    cursor=dto.cursor,
                )
            return self.uow.products.list(
                filters=filters,
                limit=dto.limit,
                direction=dto.direction,
                cursor=dto.cursor,
            )
