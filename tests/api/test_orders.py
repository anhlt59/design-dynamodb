from app.adapters.repositories import OrderRepository, ProductRepository
from app.services import OrderService

order_service = OrderService(OrderRepository(), ProductRepository())


def test_get_order(test_client, dummy_order):
    rv = test_client.get(f"/api/v1/users/{dummy_order.userId}/orders/{dummy_order.id}")
    assert rv.status_code == 200
    assert rv.json()["id"] == dummy_order.id


def test_list_order(test_client, dummy_order):
    rv = test_client.get(f"/api/v1/users/{dummy_order.userId}/orders")
    assert rv.status_code == 200
    assert len(rv.json()["items"]) == 1


def test_create_order(test_client, dummy_user, dummy_product):
    data = {
        "userId": dummy_user.id,
        "items": [{"productId": dummy_product.id, "quantity": 1, "price": dummy_product.price}],
        "address": "Test Address",
    }
    rv = test_client.post(f"/api/v1/users/{dummy_user.id}/orders", json=data)
    assert rv.status_code == 201
    order_service.delete(dummy_user.id, rv.json()["id"])
    # out of stock
    data["items"][0]["quantity"] = 100
    rv = test_client.post(f"/api/v1/users/{dummy_user.id}/orders", json=data)
    assert rv.status_code == 422


def test_cancel_order(test_client, dummy_order):
    rv = test_client.put(f"/api/v1/users/{dummy_order.userId}/orders/{dummy_order.id}")
    assert rv.status_code == 200

    order = order_service.get(dummy_order.userId, dummy_order.id)
    assert order.status == "CANCELED"
