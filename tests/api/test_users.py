from app.adapters.repositories import UserRepository
from app.db.models import UserModel
from app.services import UserService
from app.utils.datetime_utils import current_utc_timestamp

user_repository = UserRepository()
user_service = UserService(user_repository)


def test_get_user(test_client, dummy_user):
    rv = test_client.get(f"/api/v1/users/{dummy_user.id}")
    assert rv.status_code == 200
    assert rv.json()["id"] == dummy_user.id
    # not found case
    rv = test_client.get(f"/api/v1/users/123")
    assert rv.status_code == 404


def test_paginate_users(test_client):
    models = [UserModel(email=f"test{i}@gmail.com", name=f"test{i}", password="12345678") for i in range(3)]
    user_repository.batch_put(models)

    rv = test_client.get("/api/v1/users?limit=2")
    assert rv.status_code == 200
    assert len(rv.json()["items"]) == 2
    assert (cusor := rv.json()["next"]) is not None

    rv = test_client.get(f"/api/v1/users?limit=2&cursor={cusor}")
    assert rv.status_code == 200 and len(rv.json()["items"]) == 1
    assert rv.json()["previous"] == cusor
    assert rv.json()["next"] is None

    user_repository.batch_delete(models)


def test_filter_users(test_client):
    created_at = current_utc_timestamp() - 1
    models = [
        UserModel(email=f"test1@gmail.com", name=f"test1", password="12345678"),
        UserModel(email=f"test2@gmail.com", name=f"test2", password="12345678"),
        UserModel(email=f"test3@gmail.com", name=f"test3", password="12345678"),
    ]
    user_repository.batch_put(models)

    # filter by name ------------------------------------
    rv = test_client.get("/api/v1/users?name=test")
    assert rv.status_code == 200 and len(rv.json()["items"]) == 3

    # filter by since  until------------------------------
    rv = test_client.get(f"/api/v1/users?since={created_at}")
    assert rv.status_code == 200 and len(rv.json()["items"]) == 3
    rv = test_client.get(f"/api/v1/users?until={created_at}")
    assert rv.status_code == 200 and len(rv.json()["items"]) == 0

    user_repository.batch_delete(models)


def test_register_login_user(test_client):
    data = {"email": "test01@gmail.com", "name": "test01", "password": "12345678"}
    rv = test_client.post("/api/v1/users", json=data)
    assert rv.status_code == 201
    user_id = rv.json()["id"]
    # duplicate email
    rv = test_client.post("/api/v1/users", json=data)
    assert rv.status_code == 409

    user = user_service.login("test01@gmail.com", "12345678")
    assert user.id == user_id
    user_service.delete(user_id)


def test_update_user(test_client, dummy_user):
    rv = test_client.put(f"/api/v1/users/{dummy_user.id}", json={"name": "test01"})
    assert rv.status_code == 200
    user = user_service.get_by_id(dummy_user.id)
    assert user.name == "test01"

    # not found case
    rv = test_client.put(f"/api/v1/users/123", json={"name": "test01"})
    assert rv.status_code == 404


def test_delete_user(test_client, dummy_user):
    # normal case
    rv = test_client.delete(f"/api/v1/users/{dummy_user.id}")
    assert rv.status_code == 200
    # not found case
    rv = test_client.delete(f"/api/v1/users/{dummy_user.id}")
    assert rv.status_code == 404
