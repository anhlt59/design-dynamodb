from typing import Iterable

from app.adapters.db.models import (
    BrandModel,
    CategoryModel,
    DynamoModel,
    OrderItemModel,
    OrderModel,
    ProductModel,
    UserModel,
)
from app.domain.models import Brand, Category, Entity, Order, Product, User


class BaseMapper[M: DynamoModel, E: Entity]:
    @classmethod
    def to_peristence(cls, entity) -> M:
        raise NotImplementedError

    @classmethod
    def to_entity(cls, persistence) -> E:
        raise NotImplementedError

    @classmethod
    def to_peristences(cls, entities: Iterable[E]) -> list[M]:
        return [cls.to_peristence(entity) for entity in entities]

    @classmethod
    def to_entities(cls, persistences: Iterable[M]) -> list[E]:
        return [cls.to_entity(persistence) for persistence in persistences]


class BrandMapper(BaseMapper):
    @classmethod
    def to_peristence(cls, entity: Brand) -> BrandModel:
        return BrandModel(
            id=entity.id,
            name=entity.name,
            createdAt=entity.createdAt,
            updatedAt=entity.updatedAt,
        )

    @classmethod
    def to_entity(cls, persistence: BrandModel) -> Brand:
        return Brand(
            id=persistence.id,
            name=persistence.name,
            createdAt=persistence.createdAt,
            updatedAt=persistence.updatedAt,
        )


class CategoryMapper(BaseMapper):
    @classmethod
    def to_peristence(cls, entity: Category) -> CategoryModel:
        return CategoryModel(
            id=entity.id,
            name=entity.name,
            createdAt=entity.createdAt,
            updatedAt=entity.updatedAt,
        )

    @classmethod
    def to_entity(cls, persistence: CategoryModel) -> Category:
        return Category(
            id=persistence.id,
            name=persistence.name,
            createdAt=persistence.createdAt,
            updatedAt=persistence.updatedAt,
        )


class OrderMapper(BaseMapper):
    @classmethod
    def to_peristence(cls, entity: Order) -> OrderModel:
        return OrderModel(
            id=entity.id,
            userId=entity.userId,
            items=[
                OrderItemModel(
                    productId=item.productId,
                    quantity=item.quantity,
                    price=item.price,
                )
                for item in entity.items
            ],
            address=entity.address,
            status=entity.status,
            createdAt=entity.createdAt,
            updatedAt=entity.updatedAt,
        )

    @classmethod
    def to_entity(cls, persistence: OrderModel) -> Order:
        return Order(
            id=persistence.id,
            userId=persistence.userId,
            items=persistence.items,  # type: ignore
            address=persistence.address,
            status=persistence.status,  # type: ignore
            createdAt=persistence.createdAt,
            updatedAt=persistence.updatedAt,
        )


class ProductMapper(BaseMapper):
    @classmethod
    def to_peristence(cls, entity: Product) -> ProductModel:
        return ProductModel(
            id=entity.id,
            name=entity.name,
            price=entity.price,
            stock=entity.stock,
            brandId=entity.brandId,
            categoryId=entity.categoryId,
            createdAt=entity.createdAt,
            updatedAt=entity.updatedAt,
        )

    @classmethod
    def to_entity(cls, persistence: ProductModel) -> Product:
        return Product(
            id=persistence.id,
            name=persistence.name,
            price=persistence.price,
            stock=persistence.stock,
            brandId=persistence.brandId,
            categoryId=persistence.categoryId,
            createdAt=persistence.createdAt,
            updatedAt=persistence.updatedAt,
        )


class UserMapper(BaseMapper):
    @classmethod
    def to_peristence(cls, entity: User) -> UserModel:
        return UserModel(
            id=entity.id,
            name=entity.name,
            email=entity.email,
            password=entity.password,
            createdAt=entity.createdAt,
            updatedAt=entity.updatedAt,
        )

    @classmethod
    def to_entity(cls, persistence: UserModel) -> User:
        return User(
            id=persistence.id,
            name=persistence.name,
            email=persistence.email,
            password=persistence.password,
            createdAt=persistence.createdAt,
            updatedAt=persistence.updatedAt,
        )
