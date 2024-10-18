from typing import Protocol, Self

from app.domain.ports.repositories import IBrandRepository, IProductRepository


class IBrandUnitOfWork(Protocol):
    brands: IBrandRepository
    products: IProductRepository

    def __enter__(self) -> Self:
        ...

    def __exit__(self, *args):
        ...

    def commit(self):
        ...
