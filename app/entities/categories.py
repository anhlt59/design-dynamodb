from .base import BaseEntity


class CategoryEntity(BaseEntity):
    name: str
    createdAt: int
    updatedAt: int
