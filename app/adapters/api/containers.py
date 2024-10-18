from dependency_injector import containers, providers

from app.domain.adapters.repositories import (
    BrandRepository,
    CategoryRepository,
    OrderRepository,
    ProductRepository,
    UserRepository,
)
from app.domain.adapters.unit_of_works import (
    BrandUnitOfWork,
    CategoryUnitOfWork,
    OrderUnitOfWork,
    ProductUnitOfWork,
    UserUnitOfWork,
)
from app.domain.adapters.use_cases import BrandUseCase, CategoryUseCase, OrderUseCase, ProductUseCase, UserUseCase


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.adapters.api.controllers.v1.brands",
            "app.adapters.api.controllers.v1.categories",
            "app.adapters.api.controllers.v1.orders",
            "app.adapters.api.controllers.v1.products",
            "app.adapters.api.controllers.v1.users",
        ]
    )
    # Repositories
    user_repository = providers.Factory(UserRepository)
    category_repository = providers.Factory(CategoryRepository)
    brand_repository = providers.Factory(BrandRepository)
    product_repository = providers.Factory(ProductRepository)
    order_repository = providers.Factory(OrderRepository)
    # Unit of Works
    user_uow = providers.Factory(UserUnitOfWork, user_repository=user_repository)
    category_uow = providers.Factory(CategoryUnitOfWork, category_repository=category_repository)
    brand_uow = providers.Factory(
        BrandUnitOfWork, brand_repository=brand_repository, product_repository=product_repository
    )
    product_uow = providers.Factory(
        ProductUnitOfWork,
        product_repository=product_repository,
        brand_repository=brand_repository,
        category_repository=category_repository,
    )
    order_uow = providers.Factory(
        OrderUnitOfWork, order_repository=order_repository, product_repository=product_repository
    )
    # Use Cases
    user_use_case = providers.Factory(UserUseCase, uow=user_uow)
    category_use_case = providers.Factory(CategoryUseCase, uow=category_uow)
    brand_use_case = providers.Factory(BrandUseCase, uow=brand_uow)
    product_use_case = providers.Factory(ProductUseCase, uow=product_uow)
    order_use_case = providers.Factory(OrderUseCase, uow=order_uow)
