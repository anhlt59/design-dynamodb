from pynamodb.models import ResultIterator

from app.adapters.repositories import BrandRepository, ProductRepository
from app.common.exceptions import ConflictException
from app.db.models import BrandModel, ProductModel


class BrandService:
    def __init__(self, brand_repository: BrandRepository, product_repository: ProductRepository):
        self.brand_repository = brand_repository
        self.product_repository = product_repository

    def get(self, brand_id: str) -> BrandModel:
        return self.brand_repository.get(hash_key="BRAND", range_key=brand_id)

    def list(
        self,
        filters: dict | None = None,
        limit: int = 50,
        direction: str = "asc",
        cursor: dict | None = None,
    ) -> ResultIterator[BrandModel]:
        index = range_key_condition = None
        if filters and filters.get("name"):
            index = BrandModel.lsi
            range_key_condition = BrandModel.sku.startswith(filters["name"])
        return self.brand_repository.query(
            hash_key="BRAND",
            range_key_condition=range_key_condition,
            last_evaluated_key=cursor,
            scan_index_forward="asc" == direction,
            index=index,
            limit=limit,
        )

    def create(self, name: str) -> BrandModel:
        # if brand name exists in the group, raise Exception
        if self.brand_repository.exist(name) is True:
            raise ConflictException(f"Brand {name} already exists")
        return self.brand_repository.create({"name": name})

    def update(self, brand_id: str, name: str) -> BrandModel:
        return self.brand_repository.update(hash_key="BRAND", range_key=brand_id, attributes={"name": name})

    def delete(self, brand_id: str):
        products = self.product_repository.query(hash_key=brand_id, index=ProductModel.gsi1)
        with self.product_repository.transaction() as transaction:
            # delete all product related to the brand
            for product in products:
                transaction.delete(product)
            transaction.delete(BrandModel(hash_key="BRAND", range_key=brand_id))
