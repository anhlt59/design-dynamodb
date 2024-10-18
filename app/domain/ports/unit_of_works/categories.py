from typing import Protocol, Self

from app.domain.ports.repositories import ICategoryRepository


class ICategoryUnitOfWork(Protocol):
    categories: ICategoryRepository

    def __enter__(self) -> Self:
        ...

    def __exit__(self, *args):
        ...

    def commit(self):
        ...
