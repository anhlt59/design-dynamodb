import logging

import pytest
from faker import Faker

from app.adapters.repositories import (
    BrandRepository,
    CategoryRepository,
    OrderRepository,
    ProductRepository,
    UserRepository,
)
from app.framework.bootstrap import create_app

logging.getLogger("faker").setLevel(logging.WARNING)
fake = Faker()
user_repository = UserRepository()
category_repository = CategoryRepository()
brand_repository = BrandRepository()
product_repository = ProductRepository()
order_repository = OrderRepository()


@pytest.fixture
def dummy_user():
    model = user_repository.create(
        {
            "email": fake.email(),
            "name": fake.name(),
            "password": "12345678",
        }
    )
    yield model
    model.delete()


@pytest.fixture
def dummy_category():
    model = category_repository.create({"name": "Book"})
    yield model
    model.delete()


@pytest.fixture
def dummy_brand():
    model = brand_repository.create({"name": "Wiley"})
    yield model
    model.delete()


@pytest.fixture
def dummy_product(dummy_brand, dummy_category):
    model = product_repository.create(
        {
            "name": "Atomic Habits",
            "price": 13,
            "stock": 3,
            "categoryId": dummy_category.id,
            "brandId": dummy_brand.id,
        }
    )
    yield model
    model.delete()


@pytest.fixture
def dummy_order(dummy_user, dummy_product):
    model = order_repository.create(
        {
            "userId": dummy_user.id,
            "items": [{"productId": dummy_product.id, "quantity": 1, "price": dummy_product.price}],
            "address": fake.address(),
            "totalPrice": dummy_product.price,
        }
    )
    yield model
    model.delete()


@pytest.fixture
def test_client():
    app = create_app()
    with app.app_context():
        yield app.test_client()
