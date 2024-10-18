from typing import Protocol, Self

from app.domain.ports.repositories import IBrandRepository, ICategoryRepository, IProductRepository


class IProductUnitOfWork(Protocol):
    products: IProductRepository
    brands: IBrandRepository
    categories: ICategoryRepository

    def __enter__(self) -> Self:
        ...

    def __exit__(self, *args):
        ...

    def commit(self):
        ...
