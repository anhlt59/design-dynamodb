import logging

import pytest
from faker import Faker
from fastapi.testclient import TestClient

from app.adapters.api.bootstrap import create_app
from app.adapters.db.models import BrandModel, CategoryModel, OrderModel, ProductModel, UserModel
from app.common.configs import API_KEY
from app.domain.adapters.repositories import (
    BrandRepository,
    CategoryRepository,
    OrderRepository,
    ProductRepository,
    UserRepository,
)

logging.getLogger("faker").setLevel(logging.WARNING)

app = create_app()
fake = Faker()

user_repository = UserRepository()
category_repository = CategoryRepository()
brand_repository = BrandRepository()
product_repository = ProductRepository()
order_repository = OrderRepository()


@pytest.fixture
def test_client():
    with TestClient(app) as test_client:
        test_client.headers.update({"x-api-key": API_KEY})
        yield test_client


# User -------------------------------------------------------------------
@pytest.fixture
def dummy_user():
    model = UserModel(email=fake.email(), name=fake.name(), password="12345678")
    model.save()
    yield model
    # cleanup
    model.delete()


@pytest.fixture
def dummy_users():
    models = [UserModel(email=f"test{i}@gmail.com", name=f"test{i}", password="12345678") for i in range(3)]
    for model in models:
        model.save()
    yield models
    # cleanup
    for model in models:
        model.delete()


# Category -------------------------------------------------------------------


@pytest.fixture
def dummy_category():
    model = CategoryModel(name="Book")
    model.save()
    yield model
    # cleanup
    model.delete()


# Brand -------------------------------------------------------------------


@pytest.fixture
def dummy_brand():
    model = BrandModel(name="Wiley")
    model.save()
    yield model
    # cleanup
    model.delete()


# Product -------------------------------------------------------------------


@pytest.fixture
def dummy_product(dummy_brand, dummy_category):
    model = ProductModel(
        name="Atomic Habits",
        price=13,
        stock=3,
        categoryId=dummy_category.id,
        brandId=dummy_brand.id,
    )
    model.save()
    yield model
    # cleanup
    model.delete()


@pytest.fixture
def dummy_products(dummy_brand, dummy_category):
    models = [
        ProductModel(name="PRO1", price=1, stock=1, brandId=dummy_brand.id, categoryId=dummy_category.id),
        ProductModel(name="PRO2", price=2, stock=2, brandId=dummy_brand.id, categoryId=dummy_category.id),
        ProductModel(name="PRO3", price=3, stock=3, brandId="123", categoryId="123"),
    ]
    for model in models:
        model.save()
    yield models
    # cleanup
    for model in models:
        model.delete()


# Order -------------------------------------------------------------------


@pytest.fixture
def dummy_order(dummy_user, dummy_product):
    model = OrderModel(
        userId=dummy_user.id,
        items=[{"productId": dummy_product.id, "quantity": 1, "price": dummy_product.price}],
        address=fake.address(),
    )
    model.save()
    yield model
    # cleanup
    model.delete()
