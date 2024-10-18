from app.domain.ports.repositories import IBrandRepository, ICategoryRepository, IProductRepository

from .base import BaseUnitOfWork


class ProductUnitOfWork(BaseUnitOfWork):
    products: IProductRepository
    brands: IBrandRepository
    categories: ICategoryRepository

    def __init__(
        self,
        product_repository: IProductRepository,
        brand_repository: IBrandRepository,
        category_repository: ICategoryRepository,
    ):
        self.products = product_repository
        self.brands = brand_repository
        self.categories = category_repository

    def __enter__(self):
        super().__enter__()
        self.products.set_transaction(self._transaction)
        self.brands.set_transaction(self._transaction)
        self.categories.set_transaction(self._transaction)
        return self
