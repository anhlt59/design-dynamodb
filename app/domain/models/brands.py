from pydantic import BaseModel

from .base import Entity, PaginationInputDTO, PaginationOutputDTO


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


class PaginatedBrandInputDto(PaginationInputDTO):
    name: str | None = None


PaginatedBrandOutputDto = PaginationOutputDTO[BrandOutputDto]
