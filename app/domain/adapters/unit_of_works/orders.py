from app.domain.ports.repositories import IOrderRepository, IProductRepository

from .base import BaseUnitOfWork


class OrderUnitOfWork(BaseUnitOfWork):
    orders: IOrderRepository
    products: IProductRepository

    def __init__(self, order_repository: IOrderRepository, product_repository: IProductRepository):
        self.orders = order_repository
        self.products = product_repository

    def __enter__(self):
        super().__enter__()
        self.orders.set_transaction(self._transaction)
        self.products.set_transaction(self._transaction)
        return self
