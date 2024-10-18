from app.common.exceptions.http import NotFoundException
from app.domain.adapters.unit_of_works import ProductUnitOfWork
from app.domain.models import Product
from app.domain.models.products import CreateProductInputDto, PaginatedProductInputDto, UpdateProductInputDto


class ProductUseCase:
    def __init__(self, uow: ProductUnitOfWork):
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

    def list(self, dto: PaginatedProductInputDto):
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
