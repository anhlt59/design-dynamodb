from typing import Protocol

from app.domain.models import CreateUserInputDto, PaginatedOutputDTO, PaginatedUserInputDto, UpdateUserInputDto, User


class IUserUseCase(Protocol):
    def get_by_id(self, id: str) -> User:
        ...

    def get_by_email(self, email: str) -> User:
        ...

    def list(self, dto: PaginatedUserInputDto) -> PaginatedOutputDTO[User]:
        ...

    def login(self, email: str, password: str) -> User:
        ...

    def register(self, dto: CreateUserInputDto) -> User:
        ...

    def update(self, id: str, dto: UpdateUserInputDto):
        ...

    def delete(self, id: str):
        ...
