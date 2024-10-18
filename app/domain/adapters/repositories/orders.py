from app.adapters.db.models import OrderModel
from app.adapters.mappers import OrderMapper
from app.common.utils.datetime_utils import timestamp_to_hex
from app.domain.models import Order, PaginatedOutputDTO

from .base import DynamoRepository


class OrderRepository(DynamoRepository):
    model_cls = OrderModel

    def get(self, user_id: str, order_id: str) -> Order:
        model = self._get(hash_key=user_id, range_key=order_id)
        return OrderMapper.to_entity(model)

    def list(
        self,
        user_id: str,
        filters: dict | None = None,
        direction: str = "asc",
        cursor: dict | None = None,
        limit: int = 50,
    ) -> PaginatedOutputDTO[Order]:
        range_key_condition = filter_condition = None
        if filters is not None:
            # filter by createdAt
            since = filters.get("since")
            until = filters.get("until")
            if since and until:
                range_key_condition = OrderModel.sk.between(timestamp_to_hex(since), timestamp_to_hex(until))
            elif since:
                range_key_condition = OrderModel.sk >= timestamp_to_hex(since)  # type: ignore
            elif until:
                range_key_condition = OrderModel.sk < timestamp_to_hex(until)  # type: ignore
            else:
                range_key_condition = OrderModel.sk.startswith("")  # type: ignore
            # filter_condition by status
            if status := filters.get("status"):
                filter_condition = OrderModel.status == status
        result = self._query(
            hash_key=user_id,
            range_key_condition=range_key_condition,
            filter_condition=filter_condition,
            scan_index_forward="asc" == direction,
            last_evaluated_key=cursor,
            limit=limit,
        )
        return PaginatedOutputDTO(
            items=OrderMapper.to_entities(result),
            next=result.last_evaluated_key,
            previous=cursor,
            limit=limit,
        )

    def create(self, entity: Order):
        model = OrderMapper.to_peristence(entity)
        self._create(model)

    def delete(self, user_id: str, order_id: str):
        self._delete(hash_key=user_id, range_key=order_id)

    def update(self, user_id: str, order_id: str, attributes: dict):
        self._update(hash_key=user_id, range_key=order_id, attributes=attributes)
