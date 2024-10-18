from pydantic import BaseModel

from .base import Entity, PaginatedInputDTO


class Category(Entity):
    name: str


# DTOs -----------------------------------------------------
class CreateCategoryInputDto(BaseModel):
    name: str


class UpdateCategoryInputDto(BaseModel):
    name: str


class CategoryOutputDto(BaseModel):
    id: str
    name: str
    createdAt: int
    updatedAt: int


class PaginatedCategoryInputDto(PaginatedInputDTO):
    name: str | None = None
