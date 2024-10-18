from fastapi import APIRouter

from .brands import router as brand_router
from .categories import router as category_router
from .orders import router as order_router
from .products import router as product_router
from .users import router as user_router

# API V1
router = APIRouter(prefix="/v1")
router.include_router(brand_router)
router.include_router(category_router)
router.include_router(product_router)
router.include_router(order_router)
router.include_router(user_router)

__all__ = ["router"]
