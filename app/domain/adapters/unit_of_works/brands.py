from app.domain.adapters.repositories import BrandRepository, ProductRepository

from .base import BaseUnitOfWork


class BrandUnitOfWork(BaseUnitOfWork):
    def __enter__(self):
        super().__enter__()
        self.brands = BrandRepository(self.transaction)
        self.products = ProductRepository(self.transaction)
        return self
