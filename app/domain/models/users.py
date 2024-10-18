from pydantic import BaseModel

from .base import Entity, PaginatedInputDTO


class User(Entity):
    name: str
    email: str
    password: str


# DTOs -----------------------------------------------------
class CreateUserInputDto(BaseModel):
    name: str
    email: str
    password: str


class UpdateUserInputDto(BaseModel):
    name: str | None = None
    password: str | None = None
    email: str | None = None


class UserOutputDto(BaseModel):
    id: str
    name: str
    email: str
    createdAt: int
    updatedAt: int


class PaginatedUserInputDto(PaginatedInputDTO):
    name: str | None = None
    since: int | None = None
    until: int | None = None
