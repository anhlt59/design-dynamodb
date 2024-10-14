from app.adapters.repositories import CategoryRepository
from app.services import CategoryService

brand_service = CategoryService(CategoryRepository())


def test_get_category(test_client, dummy_category):
    rv = test_client.get(f"/api/v1/categories/{dummy_category.id}")
    assert rv.status_code == 200
    assert rv.json()["id"] == dummy_category.id
    # not found case
    rv = test_client.get(f"/api/v1/categories/123")
    assert rv.status_code == 404


def test_list_category(test_client, dummy_category):
    rv = test_client.get("/api/v1/categories")
    assert rv.status_code == 200
    assert len(rv.json()["items"]) == 1


def test_create_category(test_client):
    rv = test_client.post("/api/v1/categories", json={"name": "Test Category"})
    assert rv.status_code == 201
    brand_service.delete(rv.json()["id"])


def test_update_category(test_client, dummy_category):
    rv = test_client.put(f"/api/v1/categories/{dummy_category.id}", json={"name": "Test Category"})
    assert rv.status_code == 200
    assert rv.json()["id"] == dummy_category.id

    brand = brand_service.get(dummy_category.id)
    assert brand.name == "Test Category"
