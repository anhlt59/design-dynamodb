from pynamodb.exceptions import TransactWriteError

from src.exceptions import ConflictError, NotFoundError
from src.models import BrandModel, CategoryModel, ProductModel
from src.repositories import ProductRepository
from src.utils.datetime_utils import ksuid_to_timestamp, timestamp_to_hex


class ProductService:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def get(self, product_id: str) -> ProductModel:
        return self.product_repository.get(hash_key="PROD", range_key=product_id)

    def create(self, attribute: dict) -> ProductModel:
        category_id = attribute["categoryId"]
        brand_id = attribute["brandId"]
        try:
            with self.product_repository.transaction() as transaction:
                # check if category and brand exist
                transaction.condition_check(
                    CategoryModel,
                    hash_key="CAT",
                    range_key=category_id,
                    condition=CategoryModel.pk.exists() & CategoryModel.sk.exists(),
                )
                transaction.condition_check(
                    BrandModel,
                    hash_key="BRAND",
                    range_key=brand_id,
                    condition=BrandModel.pk.exists() & BrandModel.sk.exists(),
                )
                # create product
                product = ProductModel(
                    name=attribute["name"],
                    price=attribute["price"],
                    stock=attribute["stock"],
                    categoryId=category_id,
                    brandId=brand_id,
                )
                transaction.save(product)
            return product
        except TransactWriteError as err:
            error_msgs = []
            if err.cancellation_reasons[0] is not None:
                error_msgs.append(f"Category<{category_id}> not found")
            if err.cancellation_reasons[1] is not None:
                error_msgs.append(f"Brand<{brand_id}> not found")
            raise NotFoundError(", ".join(error_msgs))

    def update(self, product_id: str, attributes: dict):
        created_at = ksuid_to_timestamp(product_id)
        if brand_id := attributes.get("brandId"):
            attributes["gsi1pk"] = brand_id
            attributes["gsi2sk"] = f"{brand_id}#AT#{created_at}"
        if category_id := attributes.get("categoryId"):
            attributes["gsi2pk"] = category_id
            attributes["gsi1sk"] = f"{category_id}#AT#{created_at}"
        self.product_repository.update(hash_key="PROD", range_key=product_id, attributes=attributes)

    def increase_stock(self, product_id: str, n: int):
        self.product_repository.update(
            hash_key="PROD", range_key=product_id, actions=[ProductModel.stock.set(ProductModel.stock + n)]
        )

    def decrease_stock(self, product_id: str, n: int):
        self.product_repository.update(
            hash_key="PROD",
            range_key=product_id,
            actions=[ProductModel.stock.set(ProductModel.stock - n)],
            condition=ProductModel.stock >= n,
        )

    def delete(self, product_id: str):
        try:
            self.product_repository.delete(hash_key="PROD", range_key=product_id)
        except ConflictError:
            raise NotFoundError(f"Product<{product_id}> not found")

    def list(
        self,
        filters: dict | None = None,
        derection: str = "asc",
        cursor: dict | None = None,
        limit: int = 50,
    ):
        range_key_condition = filter_condition = None
        # set range_key_condition, filter by createdAt
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
        return self.product_repository.query(
            hash_key="PROD",
            range_key_condition=range_key_condition,
            filter_condition=filter_condition,
            scan_index_forward="asc" == derection,
            last_evaluated_key=cursor,
            limit=limit,
        )

    def list_by_brand(
        self,
        brand_id: str,
        filters: dict | None = None,
        derection: str = "asc",
        cursor: dict | None = None,
        limit: int = 50,
    ):
        range_key_condition = filter_condition = None
        # set range_key_condition
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
            filter_condition &= ProductModel.createdAt >= timestamp_to_hex(since)
        elif until:
            filter_condition &= ProductModel.createdAt < timestamp_to_hex(until)
        return self.product_repository.query(
            hash_key=brand_id,
            range_key_condition=range_key_condition,
            filter_condition=filter_condition,
            index=ProductModel.gsi1,
            scan_index_forward="asc" == derection,
            last_evaluated_key=cursor,
            limit=limit,
        )

    def list_by_category(
        self,
        category_id: str,
        filters: dict | None = None,
        derection: str = "asc",
        cursor: dict | None = None,
        limit: int = 50,
    ):
        range_key_condition = filter_condition = None
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
            filter_condition &= ProductModel.createdAt >= timestamp_to_hex(since)
        elif until:
            filter_condition &= ProductModel.createdAt < timestamp_to_hex(until)
        return self.product_repository.query(
            hash_key=category_id,
            range_key_condition=range_key_condition,
            filter_condition=filter_condition,
            index=ProductModel.gsi2,
            scan_index_forward="asc" == derection,
            last_evaluated_key=cursor,
            limit=limit,
        )
