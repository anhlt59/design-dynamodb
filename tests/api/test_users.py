from app.common.utils.datetime_utils import current_utc_timestamp


def test_get_user(test_client, dummy_user):
    rv = test_client.get(f"/api/v1/users/{dummy_user.id}")
    assert rv.status_code == 200
    assert rv.json()["id"] == dummy_user.id
    # not found case
    rv = test_client.get(f"/api/v1/users/123")
    assert rv.status_code == 404


def test_paginate_users(test_client, dummy_users):
    rv = test_client.get("/api/v1/users?limit=2")
    assert rv.status_code == 200
    assert len(rv.json()["items"]) == 2
    assert (cusor := rv.json()["next"]) is not None

    rv = test_client.get(f"/api/v1/users?limit=2&cursor={cusor}")
    assert rv.status_code == 200 and len(rv.json()["items"]) == 1
    assert rv.json()["previous"] == cusor
    assert rv.json()["next"] is None


def test_filter_users(test_client, dummy_users):
    created_at = current_utc_timestamp() - 1
    # filter by name ------------------------------------
    rv = test_client.get("/api/v1/users?name=test")
    assert rv.status_code == 200 and len(rv.json()["items"]) == 3

    # filter by since  until------------------------------
    rv = test_client.get(f"/api/v1/users?since={created_at}")
    assert rv.status_code == 200 and len(rv.json()["items"]) == 3
    rv = test_client.get(f"/api/v1/users?until={created_at}")
    assert rv.status_code == 200 and len(rv.json()["items"]) == 0


def test_register_login_user(app_context, test_client):
    data = {"email": "test01@gmail.com", "name": "test01", "password": "12345678"}
    rv = test_client.post("/api/v1/users", json=data)
    assert rv.status_code == 201
    user_id = rv.json()["id"]
    # duplicate email
    rv = test_client.post("/api/v1/users", json=data)
    assert rv.status_code == 409

    user = app_context.user_use_case.login("test01@gmail.com", "12345678")
    assert user.id == user_id
    app_context.user_use_case.delete(user_id)


def test_update_user(app_context, test_client, dummy_user):
    rv = test_client.put(f"/api/v1/users/{dummy_user.id}", json={"name": "test01"})
    assert rv.status_code == 200
    user = app_context.user_use_case.get_by_id(dummy_user.id)
    assert user.name == "test01"

    # not found case
    rv = test_client.put(f"/api/v1/users/123", json={"name": "test01"})
    assert rv.status_code == 422


def test_delete_user(test_client, dummy_user):
    # normal case
    rv = test_client.delete(f"/api/v1/users/{dummy_user.id}")
    assert rv.status_code == 200
    # not found case
    rv = test_client.delete(f"/api/v1/users/{dummy_user.id}")
    assert rv.status_code == 422
