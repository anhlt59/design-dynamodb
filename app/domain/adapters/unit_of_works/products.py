from app.domain.adapters.repositories import BrandRepository, CategoryRepository, ProductRepository

from .base import BaseUnitOfWork


class ProductUnitOfWork(BaseUnitOfWork):
    def __enter__(self):
        super().__enter__()
        self.products = ProductRepository(self.transaction)
        self.brands = BrandRepository(self.transaction)
        self.categories = CategoryRepository(self.transaction)
        return self
