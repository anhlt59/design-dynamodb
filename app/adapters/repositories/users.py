from app.db.models import UserModel

from .base import DynamoRepository


class UserRepository(DynamoRepository):
    model_class = UserModel

    def exist(self, email: str):
        count = self.count(hash_key="USER", range_key_condition=UserModel.sku == email, index=UserModel.lsi)
        return count > 0
