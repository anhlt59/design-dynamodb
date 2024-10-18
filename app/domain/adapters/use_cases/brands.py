from app.common.exceptions.http import ConflictException, NotFoundException
from app.domain.models import (
    Brand,
    CreateBrandInputDto,
    PaginatedBrandInputDto,
    PaginatedOutputDTO,
    UpdateBrandInputDto,
)
from app.domain.ports.unit_of_works import IBrandUnitOfWork


class BrandUseCase:
    def __init__(self, uow: IBrandUnitOfWork):
        self.uow = uow

    def get(self, id: str) -> Brand:
        with self.uow:
            if brand := self.uow.brands.get(id):
                return brand
            raise NotFoundException(f"Brand<id={id}> not found")

    def list(self, dto: PaginatedBrandInputDto) -> PaginatedOutputDTO[Brand]:
        with self.uow:
            if dto.name:
                return self.uow.brands.list_by_name(dto.name, dto.limit, dto.direction, dto.cursor)
            return self.uow.brands.list(dto.limit, dto.direction, dto.cursor)

    def create(self, dto: CreateBrandInputDto):
        brand = Brand.model_validate(dto)
        with self.uow:
            # if brand name exists, then raise Exception
            if self.uow.brands.count_by_name(brand.name) > 0:
                raise ConflictException(f"Brand<name={brand.name}> already exists")
            self.uow.brands.create(brand)
            self.uow.commit()
        return brand

    def update(self, id: str, dto: UpdateBrandInputDto):
        if attributes := dto.model_dump(exclude_none=True):
            with self.uow:
                self.uow.brands.update(id, attributes)
                self.uow.commit()

    def delete(self, id: str):
        with self.uow:
            # delete all products of this brand
            result = self.uow.products.list_by_brand(id, limit=1000)
            for product in result.items:
                self.uow.products.delete(product.id)
            # delete brand
            self.uow.brands.delete(id)
            self.uow.commit()
