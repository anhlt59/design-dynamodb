from typing import Protocol, Self

from app.domain.ports.repositories import IUserRepository


class IUserUnitOfWork(Protocol):
    users: IUserRepository

    def __enter__(self) -> Self:
        ...

    def __exit__(self, *args):
        ...

    def commit(self):
        ...
