from dependency_injector import containers, providers

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
    # Unit of Works
    user_uow = providers.Factory(UserUnitOfWork)
    category_uow = providers.Factory(CategoryUnitOfWork)
    brand_uow = providers.Factory(BrandUnitOfWork)
    product_uow = providers.Factory(ProductUnitOfWork)
    order_uow = providers.Factory(OrderUnitOfWork)
    # Use Cases
    user_use_case = providers.Factory(UserUseCase, uow=user_uow)
    category_use_case = providers.Factory(CategoryUseCase, uow=category_uow)
    brand_use_case = providers.Factory(BrandUseCase, uow=brand_uow)
    product_use_case = providers.Factory(ProductUseCase, uow=product_uow)
    order_use_case = providers.Factory(OrderUseCase, uow=order_uow)
