from src.models import CategoryModel

from .base import DynamoRepository


class CategoryRepository(DynamoRepository):
    model_class = CategoryModel

    def exist(self, name: str):
        count = self.count(hash_key="CAT", range_key_condition=CategoryModel.sku == name, index=CategoryModel.lsi)
        return count > 0
