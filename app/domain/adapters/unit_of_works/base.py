from typing import Self

from pynamodb.exceptions import TransactWriteError
from pynamodb.transactions import TransactWrite

from app.common.exceptions.http import InternalServerError, UnprocessedException
from app.domain.adapters.repositories.base import transaction_factory


class BaseUnitOfWork:
    _transaction: TransactWrite

    def __enter__(self) -> Self:
        self._transaction = transaction_factory()
        return self

    def __exit__(self, *args):
        # self.transaction = None
        pass

    def commit(self) -> None:
        try:
            self._transaction._commit()
        except Exception as err:
            if isinstance(err, TransactWriteError):
                raise UnprocessedException(
                    f"Transaction commit failed: {err}",
                    details=[e.message if e else None for e in err.cancellation_reasons],
                )
            raise InternalServerError(f"Transaction commit failed: {err}")
