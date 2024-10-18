from app.domain.adapters.repositories import OrderRepository, ProductRepository

from .base import BaseUnitOfWork


class OrderUnitOfWork(BaseUnitOfWork):
    def __enter__(self):
        super().__enter__()
        self.orders = OrderRepository(self.transaction)
        self.products = ProductRepository(self.transaction)
        return self
