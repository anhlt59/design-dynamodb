from app.adapters.repositories import BrandRepository, ProductRepository
from app.services import BrandService

brand_service = BrandService(BrandRepository(), ProductRepository())


def test_get_brand(test_client, dummy_brand):
    rv = test_client.get(f"/api/v1/brands/{dummy_brand.id}")
    assert rv.status_code == 200
    assert rv.json()["id"] == dummy_brand.id
    # not found case
    rv = test_client.get(f"/api/v1/brands/123")
    assert rv.status_code == 404


def test_list_brand(test_client, dummy_brand):
    rv = test_client.get("/api/v1/brands")
    assert rv.status_code == 200
    assert len(rv.json()["items"]) == 1


def test_create_brand(test_client):
    rv = test_client.post("/api/v1/brands", json={"name": "Test Brand"})
    assert rv.status_code == 201
    brand_service.delete(rv.json()["id"])


def test_update_brand(test_client, dummy_brand):
    rv = test_client.put(f"/api/v1/brands/{dummy_brand.id}", json={"name": "Test Brand"})
    assert rv.status_code == 200
    brand = brand_service.get(dummy_brand.id)
    assert brand.name == "Test Brand"
