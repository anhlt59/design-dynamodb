from flask import Blueprint, jsonify, request
from injector import inject

from app.core.exceptions import NotFoundError, ValidationError
from app.core.middlewares import api_key_required
from app.services import OrderService
from app.utils.encode_utils import base64_decode_json, base64_encode_json

app = Blueprint("api/v1/users/<user_id>", __name__)


@app.route("/orders", methods=["GET"])
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


@app.route("/orders/<order_id>", methods=["GET"])
@api_key_required
@inject
def get_order(user_id: str, order_id: str, order_service: OrderService):
    if order := order_service.get(user_id, order_id):
        return jsonify(order)
    raise NotFoundError(order_id)


@app.route("/orders", methods=["POST"])
@api_key_required
@inject
def create_order(user_id: str, order_service: OrderService):
    address = request.json.get("address")
    items = request.json.get("items")
    if not address or not items:
        raise ValidationError("Address and items are required")

    order = order_service.create(user_id, address, items)
    return jsonify({"id": order.id}), 201


@app.route("/orders/<order_id>", methods=["PUT"])
@api_key_required
@inject
def cancel_order(user_id: str, order_id: str, order_service: OrderService):
    order_service.update(user_id, order_id, "CANCELED")
    return jsonify({"id": order_id})
