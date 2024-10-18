from app.adapters.db.models import BrandModel
from app.adapters.mappers import BrandMapper
from app.domain.models import Brand, PaginatedOutputDTO

from .base import DynamoRepository


class BrandRepository(DynamoRepository):
    model_cls = BrandModel

    def get(self, id: str) -> Brand:
        model = self._get(hash_key="BRAND", range_key=id)
        return BrandMapper.to_entity(model)

    def list(self, limit: int = 50, direction: str = "asc", cursor: dict | None = None) -> PaginatedOutputDTO[Brand]:
        result = self._query(
            hash_key="BRAND",
            last_evaluated_key=cursor,
            scan_index_forward="asc" == direction,
            limit=limit,
        )
        return PaginatedOutputDTO(
            items=BrandMapper.to_entities(result),
            next=result.last_evaluated_key,
            previous=cursor,
            limit=limit,
        )

    def list_by_name(
        self, name: str, limit: int = 50, direction: str = "asc", cursor: dict | None = None
    ) -> PaginatedOutputDTO[Brand]:
        result = self._query(
            hash_key="BRAND",
            range_key_condition=BrandModel.sku.startswith(name),
            last_evaluated_key=cursor,
            scan_index_forward="asc" == direction,
            limit=limit,
            index=BrandModel.lsi,
        )
        return PaginatedOutputDTO(
            items=BrandMapper.to_entities(result),
            next=result.last_evaluated_key,
            previous=cursor,
            limit=limit,
        )

    def create(self, brand: Brand):
        model = BrandMapper.to_peristence(brand)
        self._create(model)

    def update(self, id: str, attributes: dict):
        self._update(hash_key="BRAND", range_key=id, attributes=attributes)

    def delete(self, id: str):
        self._delete(hash_key="BRAND", range_key=id)

    def count_by_name(self, name: str):
        return self._count(hash_key="BRAND", range_key_condition=BrandModel.sku == name, index=BrandModel.lsi)
