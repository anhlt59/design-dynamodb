from app.models import BrandModel

from .base import DynamoRepository


class BrandRepository(DynamoRepository):
    model_class = BrandModel

    def exist(self, name: str):
        count = self.count(hash_key="BRAND", range_key_condition=BrandModel.sku == name, index=BrandModel.lsi)
        return count > 0
