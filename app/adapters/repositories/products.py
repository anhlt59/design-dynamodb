from app.db.models import ProductModel

from .base import DynamoRepository


class ProductRepository(DynamoRepository):
    model_class = ProductModel
