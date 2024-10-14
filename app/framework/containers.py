from dependency_injector import containers, providers

from app.adapters.repositories import (
    BrandRepository,
    CategoryRepository,
    OrderRepository,
    ProductRepository,
    UserRepository,
)
from app.services import BrandService, CategoryService, OrderService, ProductService, UserService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.framework.controllers.v1.brands",
            "app.framework.controllers.v1.categories",
            "app.framework.controllers.v1.orders",
            "app.framework.controllers.v1.products",
            "app.framework.controllers.v1.users",
        ]
    )
    # Repositories
    user_repository = providers.Factory(UserRepository)
    category_repository = providers.Factory(CategoryRepository)
    brand_repository = providers.Factory(BrandRepository)
    product_repository = providers.Factory(ProductRepository)
    order_repository = providers.Factory(OrderRepository)

    # Services
    user_service = providers.Factory(UserService, user_repository=user_repository)
    category_service = providers.Factory(CategoryService, category_repository=category_repository)
    brand_service = providers.Factory(
        BrandService, brand_repository=brand_repository, product_repository=product_repository
    )
    product_service = providers.Factory(ProductService, product_repository=product_repository)
    order_service = providers.Factory(
        OrderService, order_repository=order_repository, product_repository=product_repository
    )
