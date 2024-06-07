from flask import Blueprint, jsonify, request
from injector import inject

from src.exceptions import NotFoundError, ValidationError
from src.middlewares import api_key_required
from src.services import OrderService, UserService
from src.utils.encode_utils import base64_decode_json, base64_encode_json

app = Blueprint("api/v1/users", __name__)


@app.route("", methods=["GET"])
@api_key_required
@inject
def list_users(user_service: UserService):
    derection = request.args.get("derection", default="asc", type=str)
    limit = request.args.get("limit", default=20, type=int)
    base64_cusor = request.args.get("cursor", default=None, type=str)
    filters = {
        "name": request.args.get("name", default=None, type=str),
        "since": request.args.get("since", default=None, type=int),
        "until": request.args.get("until", default=None, type=int),
    }
    result = user_service.list(
        filters=filters, limit=limit, derection=derection, cursor=base64_decode_json(base64_cusor)
    )
    return jsonify(
        {
            "items": list(result),
            "page": {"limit": limit, "next": base64_encode_json(result.last_evaluated_key), "previous": base64_cusor},
        }
    )


@app.route("/<user_id>", methods=["GET"])
@api_key_required
@inject
def get_user(user_id: str, user_service: UserService):
    if user := user_service.get_by_id(user_id):
        return jsonify(user)
    raise NotFoundError(user_id)


@app.route("", methods=["POST"])
@api_key_required
@inject
def register_user(user_service: UserService):
    name = request.json.get("name")
    email = request.json.get("email")
    password = request.json.get("password")

    if not email or not name or not password:
        raise ValidationError("Email, name, and password are required")

    user = user_service.register(name, email, password)
    return jsonify({"id": user.id}), 201


@app.route("/<user_id>", methods=["PUT"])
@api_key_required
@inject
def update_user(user_id: str, user_service: UserService):
    data = {}
    if name := request.json.get("name"):
        data["name"] = name
    if email := request.json.get("email"):
        data["email"] = email
    if password := request.json.get("password"):
        data["password"] = password

    user_service.update(user_id, data)
    return jsonify({"id": user_id})


@app.route("/<user_id>", methods=["DELETE"])
@api_key_required
@inject
def delete_user(user_id: str, user_service: UserService):
    user_service.delete(user_id)
    return jsonify({"id": user_id})


@app.route("/<user_id>/orders", methods=["GET"])
@api_key_required
@inject
def list_user_orders(user_id: str, order_service: OrderService):
    derection = request.args.get("derection", default="asc", type=str)
    limit = request.args.get("limit", default=20, type=int)
    base64_cusor = request.args.get("cursor", default=None, type=str)
    filters = {
        "since": request.args.get("since", default=None, type=int),
        "until": request.args.get("until", default=None, type=int),
        "status": request.args.get("status", default=None, type=str),
    }
    result = order_service.list_orders_by_user(
        user_id, filters=filters, limit=limit, derection=derection, cursor=base64_decode_json(base64_cusor)
    )
    return jsonify(
        {
            "items": list(result),
            "page": {"limit": limit, "next": base64_encode_json(result.last_evaluated_key), "previous": base64_cusor},
        }
    )


@app.route("/<user_id>/orders/<order_id>", methods=["GET"])
@api_key_required
@inject
def get_order(user_id: str, order_id: str, order_service: OrderService):
    if order := order_service.get(user_id, order_id):
        return jsonify(order)
    raise NotFoundError(order_id)


@app.route("/<user_id>/orders", methods=["POST"])
@api_key_required
@inject
def create_order(user_id: str, order_service: OrderService):
    address = request.json.get("address")
    items = request.json.get("items")
    if not address or not items:
        raise ValidationError("Address and items are required")

    order = order_service.create(user_id, address, items)
    return jsonify({"id": order.id}), 201


@app.route("/<user_id>/orders/<order_id>", methods=["PUT"])
@api_key_required
@inject
def cancel_order(user_id: str, order_id: str, order_service: OrderService):
    order_service.update(user_id, order_id, "CANCELED")
    return jsonify({"id": order_id})
