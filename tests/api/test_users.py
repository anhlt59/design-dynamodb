from app.core.config import APP_API_KEY
from app.models import UserModel
from app.repositories import UserRepository
from app.services import UserService
from app.utils.datetime_utils import current_utc_timestamp

HEADERS = {"x-api-key": APP_API_KEY}
user_repository = UserRepository()
user_service = UserService(user_repository)


def test_get_user(test_client, dummy_user):
    rv = test_client.get(f"/api/v1/users/{dummy_user.id}", headers=HEADERS)
    assert rv.status_code == 200
    assert rv.json["id"] == dummy_user.id
    # not found case
    rv = test_client.get(f"/api/v1/users/123", headers=HEADERS)
    assert rv.status_code == 404


def test_paginate_users(test_client):
    models = [UserModel(email=f"test{i}@gmail.com", name=f"test{i}", password="12345678") for i in range(3)]
    user_repository.batch_put(models)

    response = test_client.get("/api/v1/users?limit=2", headers=HEADERS)
    assert response.status_code == 200
    assert len(response.json["items"]) == 2
    assert (cusor := response.json["page"]["next"]) is not None

    response = test_client.get(f"/api/v1/users?limit=2&cursor={cusor}", headers=HEADERS)
    assert response.status_code == 200 and len(response.json["items"]) == 1
    assert response.json["page"]["previous"] == cusor
    assert response.json["page"]["next"] is None

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
    rv = test_client.get("/api/v1/users?name=test", headers=HEADERS)
    assert rv.status_code == 200 and len(rv.json["items"]) == 3

    # filter by since  until------------------------------
    rv = test_client.get(f"/api/v1/users?since={created_at}", headers=HEADERS)
    assert rv.status_code == 200 and len(rv.json["items"]) == 3
    rv = test_client.get(f"/api/v1/users?until={created_at}", headers=HEADERS)
    assert rv.status_code == 200 and len(rv.json["items"]) == 0

    user_repository.batch_delete(models)


def test_register_login_user(test_client):
    data = {"email": "test01@gmail.com", "name": "test01", "password": "12345678"}
    rv = test_client.post("/api/v1/users", json=data, headers=HEADERS)
    assert rv.status_code == 201
    user_id = rv.json["id"]
    # duplicate email
    rv = test_client.post("/api/v1/users", json=data, headers=HEADERS)
    assert rv.status_code == 409

    user = user_service.login("test01@gmail.com", "12345678")
    assert user.id == user_id
    user_service.delete(user_id)


def test_update_user(test_client, dummy_user):
    response = test_client.put(f"/api/v1/users/{dummy_user.id}", json={"name": "test01"}, headers=HEADERS)
    assert response.status_code == 200
    user = user_service.get_by_id(dummy_user.id)
    assert user.name == "test01"

    # not found case
    response = test_client.put(f"/api/v1/users/123", json={"name": "test01"}, headers=HEADERS)
    assert response.status_code == 404


def test_delete_user(test_client, dummy_user):
    # normal case
    response = test_client.delete(f"/api/v1/users/{dummy_user.id}", headers=HEADERS)
    assert response.status_code == 200
    # not found case
    response = test_client.delete(f"/api/v1/users/{dummy_user.id}", headers=HEADERS)
    assert response.status_code == 404
