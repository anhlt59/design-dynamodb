from typing import Protocol, Self

from app.domain.ports.repositories import IOrderRepository, IProductRepository


class IOrderUnitOfWork(Protocol):
    orders: IOrderRepository
    products: IProductRepository

    def __enter__(self) -> Self:
        ...

    def __exit__(self, *args):
        ...

    def commit(self):
        ...
