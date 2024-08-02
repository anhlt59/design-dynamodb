from .base import BaseEntity


class UserEntity(BaseEntity):
    name: str
    email: str
    password: str
    createdAt: int
    updatedAt: int
