from src.config import APP_API_KEY
from src.models import ProductModel
from src.repositories import CategoryRepository, ProductRepository
from src.services import CategoryService, ProductService

HEADERS = {"x-api-key": APP_API_KEY}
product_repository = ProductRepository()
category_repository = CategoryRepository()
product_service = ProductService(product_repository)
category_service = CategoryService(category_repository)


def test_get_product(test_client, dummy_product):
    rv = test_client.get(f"/api/v1/products/{dummy_product.id}", headers=HEADERS)
    assert rv.status_code == 200
    assert rv.json["id"] == dummy_product.id


def test_list_product(test_client, dummy_brand, dummy_category):
    models = [
        ProductModel(name="PRO1", price=1, stock=1, brandId=dummy_brand.id, categoryId=dummy_category.id),
        ProductModel(name="PRO2", price=2, stock=2, brandId=dummy_brand.id, categoryId=dummy_category.id),
        ProductModel(name=f"PRO3", price=3, stock=3, brandId="123", categoryId="123"),
    ]
    product_repository.batch_put(models)

    rv = test_client.get("/api/v1/products", headers=HEADERS)
    assert rv.status_code == 200 and len(rv.json["items"]) == 3
    # filter by name
    rv = test_client.get("/api/v1/products?name=PRO1", headers=HEADERS)
    assert rv.status_code == 200 and len(rv.json["items"]) == 1
    # filter by price
    rv = test_client.get("/api/v1/products?priceGT=2", headers=HEADERS)
    assert rv.status_code == 200 and len(rv.json["items"]) == 1
    # filter by brand_id
    rv = test_client.get(f"/api/v1/products?brandId={dummy_brand.id}", headers=HEADERS)
    assert rv.status_code == 200 and len(rv.json["items"]) == 2
    # filter by category_id
    rv = test_client.get(f"/api/v1/products?categoryId={dummy_category.id}", headers=HEADERS)
    assert rv.status_code == 200 and len(rv.json["items"]) == 2
    # filter by brand_id and category_id
    rv = test_client.get(f"/api/v1/products?brandId=123&categoryId=123", headers=HEADERS)
    assert rv.status_code == 200 and len(rv.json["items"]) == 1

    product_repository.batch_delete(models)


def test_create_product(test_client, dummy_brand, dummy_category):
    data = {
        "name": "Test Product",
        "price": 100,
        "brandId": dummy_brand.id,
        "categoryId": dummy_category.id,
        "stock": 100,
    }
    rv = test_client.post("/api/v1/products", json=data, headers=HEADERS)
    assert rv.status_code == 201
    product_service.delete(rv.json["id"])


def test_update_product(test_client, dummy_product):
    new_category = category_service.create(name="Test Category")
    data = {"name": "Test Product", "categoryId": new_category.id}
    rv = test_client.put(f"/api/v1/products/{dummy_product.id}", json=data, headers=HEADERS)
    assert rv.status_code == 200

    brand = product_service.get(dummy_product.id)
    assert brand.name == "Test Product" and brand.categoryId == new_category.id

    new_category.delete()
