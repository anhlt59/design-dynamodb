from .brands import app as brand_controller
from .categories import app as category_controller
from .orders import app as order_controller
from .products import app as product_controller
from .users import app as user_controller

__all__ = ["brand_controller", "category_controller", "product_controller", "order_controller", "user_controller"]
