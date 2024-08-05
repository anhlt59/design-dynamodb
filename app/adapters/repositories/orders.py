from app.db.models import OrderModel

from .base import DynamoRepository


class OrderRepository(DynamoRepository):
    model_class = OrderModel
