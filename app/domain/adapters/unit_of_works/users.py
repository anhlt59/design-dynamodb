from app.domain.adapters.repositories import UserRepository

from .base import BaseUnitOfWork


class UserUnitOfWork(BaseUnitOfWork):
    def __enter__(self):
        super().__enter__()
        self.users = UserRepository(self.transaction)
        return self
