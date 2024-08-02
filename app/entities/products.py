from .base import BaseEntity


class ProductEntity(BaseEntity):
    name: str
    price: float
    stock: int
    brandId: str
    categoryId: str
    createdAt: int
    updatedAt: int
