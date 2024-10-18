from app.domain.models import Category


def test_get_product(test_client, dummy_product):
    rv = test_client.get(f"/api/v1/products/{dummy_product.id}")
    assert rv.status_code == 200
    assert rv.json()["id"] == dummy_product.id


def test_list_product(test_client, dummy_brand, dummy_category, dummy_products):
    rv = test_client.get("/api/v1/products")
    assert rv.status_code == 200 and len(rv.json()["items"]) == 3
    # filter by name
    rv = test_client.get("/api/v1/products?name=PRO1")
    assert rv.status_code == 200 and len(rv.json()["items"]) == 1
    # filter by price
    rv = test_client.get("/api/v1/products?priceGT=2")
    assert rv.status_code == 200 and len(rv.json()["items"]) == 1
    # filter by brand_id
    rv = test_client.get(f"/api/v1/products?brandId={dummy_brand.id}")
    assert rv.status_code == 200 and len(rv.json()["items"]) == 2
    # filter by category_id
    rv = test_client.get(f"/api/v1/products?categoryId={dummy_category.id}")
    assert rv.status_code == 200 and len(rv.json()["items"]) == 2
    # filter by brand_id and category_id
    rv = test_client.get(f"/api/v1/products?brandId=123&categoryId=123")
    assert rv.status_code == 200 and len(rv.json()["items"]) == 1


def test_create_product(app_context, test_client, dummy_brand, dummy_category):
    data = {
        "name": "Test Product",
        "price": 100,
        "brandId": dummy_brand.id,
        "categoryId": dummy_category.id,
        "stock": 100,
    }
    rv = test_client.post("/api/v1/products", json=data)
    assert rv.status_code == 201
    app_context.product_use_case.delete(rv.json()["id"])
    # invalid brand_id
    data["brandId"] = "INVALID_ID"
    rv = test_client.post("/api/v1/products", json=data)
    assert rv.status_code == 404


def test_update_product(app_context, test_client, dummy_product):
    app_context.category_use_case.create(new_category := Category(name="Test Category"))
    data = {"name": "Test Product", "categoryId": new_category.id}
    rv = test_client.put(f"/api/v1/products/{dummy_product.id}", json=data)
    assert rv.status_code == 200

    brand = app_context.product_use_case.get(dummy_product.id)
    assert brand.name == "Test Product" and brand.categoryId == new_category.id

    app_context.category_use_case.delete(new_category.id)
