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


def test_create_brand(app_context, test_client):
    rv = test_client.post("/api/v1/brands", json={"name": "Test Brand"})
    assert rv.status_code == 201
    app_context.brand_use_case.delete(rv.json()["id"])


def test_update_brand(app_context, test_client, dummy_brand):
    rv = test_client.put(f"/api/v1/brands/{dummy_brand.id}", json={"name": "Test Brand"})
    assert rv.status_code == 200
    brand = app_context.brand_use_case.get(dummy_brand.id)
    assert brand.name == "Test Brand"
