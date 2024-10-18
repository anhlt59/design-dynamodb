from typing import Protocol

from pynamodb.transactions import Transaction

from app.domain.models import PaginatedOutputDTO, User


class IUserRepository(Protocol):
    def set_transaction(self, transaction: Transaction):
        ...

    def get_by_id(self, id: str) -> User:
        ...

    def get_by_email(self, email: str) -> User:
        ...

    def list(
        self, filters: dict | None = None, direction: str = "asc", cursor: dict | None = None, limit: int = 50
    ) -> PaginatedOutputDTO[User]:
        ...

    def create(self, user: User):
        ...

    def delete(self, id: str):
        ...

    def update(self, id: str, attributes: dict):
        ...

    def count_by_email(self, email: str) -> int:
        ...
