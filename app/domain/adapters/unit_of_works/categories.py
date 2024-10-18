from app.domain.ports.repositories import ICategoryRepository

from .base import BaseUnitOfWork


class CategoryUnitOfWork(BaseUnitOfWork):
    categories: ICategoryRepository

    def __init__(self, category_repository: ICategoryRepository):
        self.categories = category_repository

    def __enter__(self):
        super().__enter__()
        self.categories.set_transaction(self._transaction)
        return self
