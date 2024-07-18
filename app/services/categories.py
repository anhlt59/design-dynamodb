from pynamodb.models import ResultIterator

from app.core.exceptions import ConflictError
from app.models import CategoryModel
from app.repositories import CategoryRepository


class CategoryService:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    def get(self, category_id: str) -> CategoryModel:
        return self.category_repository.get(hash_key="CAT", range_key=category_id)

    def list(
        self,
        filters: dict | None = None,
        limit: int = 50,
        derection: str = "asc",
        cursor: dict | None = None,
    ) -> ResultIterator[CategoryModel]:
        if filters and filters.get("name"):
            index = CategoryModel.lsi
            range_key_condition = CategoryModel.sku.startswith(filters["name"])
        else:
            index = range_key_condition = None
        return self.category_repository.query(
            hash_key="CAT",
            range_key_condition=range_key_condition,
            last_evaluated_key=cursor,
            scan_index_forward="asc" == derection,
            index=index,
            limit=limit,
        )

    def create(self, name: str) -> CategoryModel:
        # if category name exists in the group, raise Exception
        if self.category_repository.exist(name) is True:
            raise ConflictError(f"Category {name} already exists")
        return self.category_repository.create({"name": name})

    def update(self, category_id: str, name: str) -> CategoryModel:
        return self.category_repository.update(hash_key="CAT", range_key=category_id, attributes={"name": name})

    def delete(self, category_id: str):
        self.category_repository.delete(hash_key="CAT", range_key=category_id)
