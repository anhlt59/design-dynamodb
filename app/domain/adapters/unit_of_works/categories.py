from app.domain.adapters.repositories import CategoryRepository

from .base import BaseUnitOfWork


class CategoryUnitOfWork(BaseUnitOfWork):
    def __enter__(self):
        super().__enter__()
        self.categories = CategoryRepository(self.transaction)
        return self
