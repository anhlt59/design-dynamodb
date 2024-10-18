from app.adapters.db.models import ProductModel
from app.adapters.mappers import ProductMapper
from app.common.utils.datetime_utils import timestamp_to_hex, uuid7_to_timestamp
from app.domain.models import PaginatedOutputDTO, Product

from .base import DynamoRepository


class ProductRepository(DynamoRepository):
    model_cls = ProductModel

    def get(self, id: str) -> Product:
        model = self._get(hash_key="PROD", range_key=id)
        return ProductMapper.to_entity(model)

    def list(
        self,
        filters: dict | None = None,
        direction: str = "asc",
        cursor: dict | None = None,
        limit: int = 50,
    ) -> PaginatedOutputDTO[Product]:
        range_key_condition = filter_condition = None
        # set range_key_condition, filter by createdAt
        if filters:
            since = filters.get("since")
            until = filters.get("until")
            if since and until:
                filter_condition &= ProductModel.sk.between(timestamp_to_hex(since), timestamp_to_hex(until))
            elif since:
                filter_condition &= ProductModel.sk >= timestamp_to_hex(since)
            elif until:
                filter_condition &= ProductModel.sk < timestamp_to_hex(until)
            # filter by name
            if name := filters.get("name"):
                filter_condition &= ProductModel.name.contains(name)
            # filter by price
            price_gt = filters.get("priceGT")
            price_lt = filters.get("priceLT")
            if price_gt and price_lt:
                filter_condition &= ProductModel.price.between(price_lt, price_gt)
            elif price_lt:
                filter_condition &= ProductModel.price < price_lt
            elif price_gt:
                filter_condition &= ProductModel.price > price_gt
        result = self._query(
            hash_key="PROD",
            range_key_condition=range_key_condition,
            filter_condition=filter_condition,
            scan_index_forward="asc" == direction,
            last_evaluated_key=cursor,
            limit=limit,
        )
        return PaginatedOutputDTO(
            items=ProductMapper.to_entities(result),
            next=result.last_evaluated_key,
            previous=cursor,
            limit=limit,
        )

    def list_by_brand(
        self,
        brand_id: str,
        filters: dict | None = None,
        direction: str = "asc",
        cursor: dict | None = None,
        limit: int = 50,
    ) -> PaginatedOutputDTO[Product]:
        range_key_condition = filter_condition = None
        # set range_key_condition
        if filters:
            if category_id := filters.get("categoryId"):
                range_key_condition = ProductModel.gsi1sk.startswith(category_id)
            # filter by name
            if name := filters.get("name"):
                filter_condition &= ProductModel.name.contains(name)
            # filter by price
            price_gt = filters.get("priceGT")
            price_lt = filters.get("priceLT")
            if price_gt and price_lt:
                filter_condition &= ProductModel.price.between(price_lt, price_gt)
            elif price_lt:
                filter_condition &= ProductModel.price < price_lt
            elif price_gt:
                filter_condition &= ProductModel.price > price_gt
            # filter by createdAt
            since = filters.get("since")
            until = filters.get("until")
            if since and until:
                filter_condition &= ProductModel.createdAt.between(timestamp_to_hex(since), timestamp_to_hex(until))
            elif since:
                filter_condition &= ProductModel.createdAt >= timestamp_to_hex(since)  # type: ignore
            elif until:
                filter_condition &= ProductModel.createdAt < timestamp_to_hex(until)  # type: ignore
        result = self._query(
            hash_key=brand_id,
            range_key_condition=range_key_condition,
            filter_condition=filter_condition,
            index=ProductModel.gsi1,
            scan_index_forward="asc" == direction,
            last_evaluated_key=cursor,
            limit=limit,
        )
        return PaginatedOutputDTO(
            items=ProductMapper.to_entities(result),
            next=result.last_evaluated_key,
            previous=cursor,
            limit=limit,
        )

    def list_by_category(
        self,
        category_id: str,
        filters: dict | None = None,
        direction: str = "asc",
        cursor: dict | None = None,
        limit: int = 50,
    ) -> PaginatedOutputDTO[Product]:
        range_key_condition = filter_condition = None
        if filters:
            # set range_key_condition
            if brand_id := filters.get("brandId"):
                range_key_condition = ProductModel.gsi1sk.startswith(brand_id)
            # filter by name
            if name := filters.get("name"):
                filter_condition &= ProductModel.name.contains(name)
            # filter by price
            price_gt = filters.get("priceGT")
            price_lt = filters.get("priceLT")
            if price_gt and price_lt:
                filter_condition &= ProductModel.price.between(price_lt, price_gt)
            elif price_lt:
                filter_condition &= ProductModel.price < price_lt
            elif price_gt:
                filter_condition &= ProductModel.price > price_gt
            # filter by createdAt
            since = filters.get("since")
            until = filters.get("until")
            if since and until:
                filter_condition &= ProductModel.createdAt.between(timestamp_to_hex(since), timestamp_to_hex(until))
            elif since:
                filter_condition &= ProductModel.createdAt >= timestamp_to_hex(since)  # type: ignore
            elif until:
                filter_condition &= ProductModel.createdAt < timestamp_to_hex(until)  # type: ignore
        result = self._query(
            hash_key=category_id,
            range_key_condition=range_key_condition,
            filter_condition=filter_condition,
            index=ProductModel.gsi2,
            scan_index_forward="asc" == direction,
            last_evaluated_key=cursor,
            limit=limit,
        )
        return PaginatedOutputDTO(
            items=ProductMapper.to_entities(result),
            next=result.last_evaluated_key,
            previous=cursor,
            limit=limit,
        )

    def create(self, entity: Product):
        model = ProductMapper.to_peristence(entity)
        return self._create(model)

    def decrease_stock(self, id: str, quantity: int):
        actions = [ProductModel.stock.set(ProductModel.stock - quantity)]
        condition = ProductModel.stock >= quantity
        self._update(hash_key="PROD", range_key=id, actions=actions, condition=condition)

    def update(self, id: str, attributes: dict):
        created_at = uuid7_to_timestamp(id)
        if brand_id := attributes.get("brandId"):
            attributes["gsi1pk"] = brand_id
            attributes["gsi2sk"] = f"{brand_id}#AT#{created_at}"
        if category_id := attributes.get("categoryId"):
            attributes["gsi2pk"] = category_id
            attributes["gsi1sk"] = f"{category_id}#AT#{created_at}"
        self._update(hash_key="PROD", range_key=id, attributes=attributes)

    def delete(self, id: str):
        self._delete(hash_key="PROD", range_key=id)
