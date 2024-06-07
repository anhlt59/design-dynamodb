from src.models import UserModel

from .base import DynamoRepository


class UserRepository(DynamoRepository):
    model_class = UserModel

    def exist(self, email: str):
        count = self.count(hash_key="USER", range_key_condition=UserModel.gsi1sk == email, index=UserModel.gsi1)
        return count > 0
