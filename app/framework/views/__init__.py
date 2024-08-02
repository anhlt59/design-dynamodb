from .brands import app as brand_view
from .categories import app as category_view
from .orders import app as order_view
from .products import app as product_view
from .users import app as user_view

__all__ = ["brand_view", "category_view", "product_view", "order_view", "user_view"]
