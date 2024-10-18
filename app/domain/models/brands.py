from pydantic import BaseModel

from .base import Entity, PaginatedInputDTO


class Brand(Entity):
    name: str


# DTOs -----------------------------------------------------
class CreateBrandInputDto(BaseModel):
    name: str


class UpdateBrandInputDto(BaseModel):
    name: str


class BrandOutputDto(BaseModel):
    id: str
    name: str
    createdAt: int
    updatedAt: int


class PaginatedBrandInputDto(PaginatedInputDTO):
    name: str | None = None
