from app.adapters.db.models import CategoryModel
from app.adapters.mappers import CategoryMapper
from app.domain.models import Category, PaginatedOutputDTO

from .base import DynamoRepository


class CategoryRepository(DynamoRepository):
    model_cls = CategoryModel

    def get(self, id: str) -> Category:
        model = self._get(hash_key="CAT", range_key=id)
        return CategoryMapper.to_entity(model)

    def list(
        self, limit: int = 50, direction: str = "asc", cursor: dict | None = None
    ) -> PaginatedOutputDTO[Category]:
        result = self._query(
            hash_key="CAT",
            last_evaluated_key=cursor,
            scan_index_forward="asc" == direction,
            limit=limit,
        )
        return PaginatedOutputDTO(
            items=CategoryMapper.to_entities(result),
            next=result.last_evaluated_key,
            previous=cursor,
            limit=limit,
        )

    def list_by_name(
        self, name: str, limit: int = 50, direction: str = "asc", cursor: dict | None = None
    ) -> PaginatedOutputDTO[Category]:
        result = self._query(
            hash_key="CAT",
            range_key_condition=CategoryModel.sku.startswith(name),
            last_evaluated_key=cursor,
            scan_index_forward="asc" == direction,
            limit=limit,
            index=CategoryModel.lsi,
        )
        return PaginatedOutputDTO(
            items=CategoryMapper.to_entities(result),
            next=result.last_evaluated_key,
            previous=cursor,
            limit=limit,
        )

    def create(self, entity: Category):
        model = CategoryMapper.to_peristence(entity)
        self._create(model)

    def update(self, id: str, attributes: dict):
        self._update(hash_key="CAT", range_key=id, attributes=attributes)

    def delete(self, id: str):
        self._delete(hash_key="CAT", range_key=id)

    def count_by_name(self, name: str):
        return self._count(hash_key="CAT", range_key_condition=CategoryModel.sku == name, index=CategoryModel.lsi)
