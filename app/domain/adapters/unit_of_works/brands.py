from app.domain.ports.repositories import IBrandRepository, IProductRepository

from .base import BaseUnitOfWork


class BrandUnitOfWork(BaseUnitOfWork):
    brands: IBrandRepository
    products: IProductRepository

    def __init__(self, brand_repository: IBrandRepository, product_repository: IProductRepository):
        self.brands = brand_repository
        self.products = product_repository

    def __enter__(self):
        super().__enter__()
        self.brands.set_transaction(self._transaction)
        self.products.set_transaction(self._transaction)
        return self
