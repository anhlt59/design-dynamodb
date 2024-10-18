from app.adapters.db.models import UserModel
from app.adapters.mappers import UserMapper
from app.common.exceptions.http import NotFoundException
from app.common.utils.datetime_utils import timestamp_to_hex
from app.domain.models import PaginatedOutputDTO, User

from .base import DynamoRepository


class UserRepository(DynamoRepository):
    model_cls = UserModel

    def get_by_id(self, id: str) -> User:
        model = self._get(hash_key="USER", range_key=id)
        return UserMapper.to_entity(model)

    def get_by_email(self, email: str) -> User:
        result = self._query(
            hash_key="USER",
            range_key_condition=UserModel.sku == email,
            index=UserModel.lsi,
        )
        if user := next(result, None):
            return UserMapper.to_entity(user)
        raise NotFoundException(f"User<email={email}> not found")

    def list(
        self,
        filters: dict | None = None,
        direction: str = "asc",
        cursor: dict | None = None,
        limit: int = 50,
    ) -> PaginatedOutputDTO[User]:
        range_key_condition = filter_condition = None
        # set range_key_condition, filter by createdAt
        if filters:
            since = filters.get("since")
            until = filters.get("until")
            if since and until:
                range_key_condition = UserModel.sk.between(timestamp_to_hex(since), timestamp_to_hex(until))
            elif since:
                range_key_condition = UserModel.sk >= timestamp_to_hex(since)  # type: ignore
            elif until:
                range_key_condition = UserModel.sk < timestamp_to_hex(until)  # type: ignore
            # filter by name
            if name := filters.get("name"):
                filter_condition = UserModel.name.contains(name)
        result = self._query(
            hash_key="USER",
            range_key_condition=range_key_condition,
            last_evaluated_key=cursor,
            scan_index_forward="asc" == direction,
            filter_condition=filter_condition,
            limit=limit,
        )
        return PaginatedOutputDTO(
            items=UserMapper.to_entities(result),
            next=result.last_evaluated_key,
            previous=cursor,
            limit=limit,
        )

    def create(self, entity: User):
        model = UserMapper.to_peristence(entity)
        return self._create(model)

    def update(self, id: str, attributes: dict):
        if email := attributes.get("email"):
            attributes["sku"] = email
        self._update(hash_key="USER", range_key=id, attributes=attributes)

    def delete(self, id: str):
        self._delete(hash_key="USER", range_key=id)

    def count_by_email(self, email: str) -> int:
        return self._count(hash_key="USER", range_key_condition=UserModel.sku == email, index=UserModel.lsi)
