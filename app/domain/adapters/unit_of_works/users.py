from app.domain.ports.repositories import IUserRepository

from .base import BaseUnitOfWork


class UserUnitOfWork(BaseUnitOfWork):
    users: IUserRepository

    def __init__(self, user_repository: IUserRepository):
        self.users = user_repository

    def __enter__(self):
        super().__enter__()
        self.users.set_transaction(self._transaction)
        return self
