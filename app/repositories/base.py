from typing import Any, Iterator, List, Type

from pynamodb.attributes import Attribute
from pynamodb.connection import Connection
from pynamodb.exceptions import (
    AttributeDeserializationError,
    AttributeNullError,
    DeleteError,
    DoesNotExist,
    GetError,
    PutError,
    QueryError,
    UpdateError,
)
from pynamodb.models import Action, Condition, Index, ResultIterator
from pynamodb.transactions import TransactWrite

from app.core.exceptions import ConflictError, InternalServerError, NotFoundError, UnprocessableEntityError
from app.models import DynamoModel
from app.models.base import DynamoMeta


class DynamoRepository[T: DynamoModel]:
    model_class: Type[T]
    hash_key_attribute: Attribute
    range_key_attribute: Attribute

    def __init__(self):
        self.hash_key_attribute = self.model_class._hash_key_attribute()
        self.range_key_attribute = self.model_class._range_key_attribute()

    # CRUD operations
    def get(self, hash_key: Any, range_key: Any = None, attributes_to_get: List[str] | None = None) -> T:
        try:
            return self.model_class.get(hash_key, range_key=range_key, attributes_to_get=attributes_to_get)
        except DoesNotExist as err:
            raise NotFoundError(f"{self.__class__.__name__}: {err}")
        except GetError as err:
            raise UnprocessableEntityError(f"{self.__class__.__name__}: {err}")
        except Exception as err:
            raise InternalServerError(f"{self.__class__.__name__}: {err}")

    def query(
        self,
        hash_key: Any,
        range_key_condition: Condition | None = None,
        index: Index | None = None,
        scan_index_forward: bool | None = None,
        filter_condition: Condition | None = None,
        attributes_to_get: List[str] | None = None,
        last_evaluated_key: dict[str, dict[str, Any]] | None = None,
        limit: int = 50,
    ) -> ResultIterator[T]:
        query_cls = index if index is not None else self.model_class
        try:
            return query_cls.query(
                hash_key,
                range_key_condition=range_key_condition,
                filter_condition=filter_condition,
                attributes_to_get=attributes_to_get,
                last_evaluated_key=last_evaluated_key,
                limit=limit,
                scan_index_forward=scan_index_forward,
            )
        except QueryError as err:
            raise UnprocessableEntityError(f"{self.__class__.__name__}: {err}")
        except Exception as err:
            raise InternalServerError(f"{self.__class__.__name__}: {err}")

    def create(self, attributes: dict, overwrite=False, condition: Condition | None = None, auto_commit=True) -> T:
        # If overwrite is False, add condition to check if the item already exists
        if overwrite is False:
            condition &= self.hash_key_attribute.does_not_exist()
            if self.range_key_attribute is not None:
                condition &= self.range_key_attribute.does_not_exist()

        try:
            model = self.model_class(**attributes)
            if auto_commit is True:
                model.save(condition=condition)
        except (AttributeNullError, AttributeDeserializationError) as err:
            raise UnprocessableEntityError(f"{self.__class__.__name__} - AttributeError: {err}")
        except PutError as err:
            if err.cause_response_code == "ConditionalCheckFailedException":
                raise ConflictError(f"{self.__class__.__name__}: {err}")
            raise UnprocessableEntityError(f"{self.__class__.__name__} - PutError: {err}")
        except Exception as err:
            raise InternalServerError(f"{self.__class__.__name__}: {err}")
        return model

    def update(
        self,
        hash_key: Any,
        range_key: Any = None,
        attributes: dict | None = None,
        actions: List[Action] | None = None,
        insert_if_not_exists=False,
        condition: Condition | None = None,
    ):
        if attributes is not None:
            if actions is None:
                actions = []
            for key, value in attributes.items():
                if attr := getattr(self.model_class, key):
                    actions.append(attr.set(value))
                else:
                    raise ValueError(f"{self.__class__.__name__}: Attribute {key} does not exist")

        # if insert_if_not_exists is True, insert new item if item does not exist
        if insert_if_not_exists is False:
            condition &= self.hash_key_attribute.exists()
            if self.range_key_attribute is not None:
                condition &= self.range_key_attribute.exists()

        try:
            model = self.model_class(hash_key=hash_key, range_key=range_key)
            model.update(actions=actions, condition=condition)
        except DoesNotExist as err:
            raise NotFoundError(f"{self.__class__.__name__}: {err}")
        except UpdateError as err:
            if err.cause_response_code == "ConditionalCheckFailedException":
                raise ConflictError(f"{self.__class__.__name__}: {err}")
            raise UnprocessableEntityError(f"{self.__class__.__name__}: {err}")
        except Exception as err:
            raise InternalServerError(f"{self.__class__.__name__}: {err}")

    def save(self, model: T) -> T:
        try:
            model.save()
        except PutError as err:
            raise UnprocessableEntityError(f"{self.__class__.__name__}: {err}")
        except Exception as err:
            raise InternalServerError(f"{self.__class__.__name__}: {err}")
        return model

    def delete(
        self,
        hash_key: Any,
        range_key: Any = None,
        ignore_if_not_exist=True,
        condition: Condition | None = None,
    ):
        # if ignore_not_exists is False, raise error if item does not exist
        if ignore_if_not_exist is False:
            condition &= self.hash_key_attribute.exists()
            if self.range_key_attribute is not None:
                condition &= self.range_key_attribute.exists()

        try:
            self.model_class(hash_key=hash_key, range_key=range_key).delete(condition=condition)
        except DeleteError as err:
            if err.cause_response_code == "ConditionalCheckFailedException":
                raise ConflictError(f"{self.__class__.__name__}: {err}")
            raise UnprocessableEntityError(f"{self.__class__.__name__}: {err}")
        except Exception as err:
            raise InternalServerError(f"{self.__class__.__name__}: {err}")

    def count(
        self,
        hash_key: Any,
        range_key_condition: Condition | None = None,
        filter_condition: Condition | None = None,
        index: Index | None = None,
    ) -> int:
        query_cls = index if index is not None else self.model_class

        try:
            return query_cls.count(hash_key, range_key_condition, filter_condition=filter_condition)
        except QueryError as err:
            raise UnprocessableEntityError(f"{self.__class__.__name__}: {err}")
        except Exception as err:
            raise InternalServerError(f"{self.__class__.__name__}: {err}")

    def batch_get(self, items: list[tuple[Any, Any]], attributes_to_get=None) -> Iterator[DynamoModel]:
        """Get items by theirs keys including prefixes."""
        return DynamoModel.batch_get(items, attributes_to_get=attributes_to_get)

    def batch_put(self, models: list[DynamoModel]):
        with DynamoModel.batch_write() as batch:
            for model in models:
                batch.save(model)

    def batch_delete(self, models: list[DynamoModel]):
        with DynamoModel.batch_write() as batch:
            for model in models:
                batch.delete(model)

    @staticmethod
    def transaction():
        connection = Connection(region=DynamoMeta.region, host=DynamoMeta.host)
        return TransactWrite(connection=connection)
