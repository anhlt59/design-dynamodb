from pydantic import BaseModel

from .base import Entity, PaginatedInputDTO


class Product(Entity):
    name: str
    price: float
    stock: int
    brandId: str
    categoryId: str


# DTOs -----------------------------------------------------
class CreateProductInputDto(BaseModel):
    name: str
    price: float
    stock: int
    categoryId: str
    brandId: str


class UpdateProductInputDto(BaseModel):
    name: str | None = None
    price: float | None = None
    stock: int | None = None
    categoryId: str | None = None
    brandId: str | None = None


class ProductOutputDto(BaseModel):
    id: str
    name: str
    price: float
    stock: int
    categoryId: str
    brandId: str
    createdAt: int
    updatedAt: int


class PaginatedProductInputDto(PaginatedInputDTO):
    name: str | None = None
    categoryId: str | None = None
    brandId: str | None = None
    priceGT: float | None = None
    priceLT: float | None = None
    since: int | None = None
    until: int | None = None
