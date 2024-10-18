from typing import Any

from app.common.exceptions.http import ConflictException, NotFoundException
from app.domain.adapters.unit_of_works import CategoryUnitOfWork
from app.domain.models.categories import (
    Category,
    CreateCategoryInputDto,
    PaginatedCategoryInputDto,
    UpdateCategoryInputDto,
)


class CategoryUseCase:
    def __init__(self, uow: CategoryUnitOfWork):
        self.uow = uow

    def get(self, id: str) -> Category:
        with self.uow:
            if category := self.uow.categories.get(id):
                return category
            raise NotFoundException(f"Category<id={id}> not found")

    def list(self, dto: PaginatedCategoryInputDto) -> tuple[list[Category], Any]:
        with self.uow:
            if dto.name:
                return self.uow.categories.list_by_name(dto.name, dto.limit, dto.direction, dto.cursor)
            return self.uow.categories.list(dto.limit, dto.direction, dto.cursor)

    def create(self, dto: CreateCategoryInputDto):
        category = Category.model_validate(dto)
        with self.uow:
            # if category name exists, then raise Exception
            if self.uow.categories.count_by_name(category.name) > 0:
                raise ConflictException(f"Category<name={category.name}> already exists")
            self.uow.categories.create(category)
            self.uow.commit()
        return category

    def update(self, id: str, dto: UpdateCategoryInputDto):
        if attributes := dto.model_dump(exclude_none=True):
            with self.uow:
                self.uow.categories.update(id, attributes)
                self.uow.commit()

    def delete(self, id: str):
        with self.uow:
            self.uow.categories.delete(id)
            self.uow.commit()
