from flask import Blueprint, request
from injector import inject

from app.adapters.presenters.base import Response
from app.adapters.presenters.orders import OrderCreateRequest, OrderResponse, OrdersRequest, OrdersResponse
from app.common.exceptions import NotFoundError
from app.framework.middlewares import api_key_required
from app.services import OrderService
from app.utils.encode_utils import base64_encode_json

app = Blueprint("orders", __name__)


@app.get("/orders")
@api_key_required
@inject
def list_user_orders(user_id: str, order_service: OrderService):
    params = OrdersRequest(**request.args)
    result = order_service.list_orders_by_user(
        user_id, filters=params.filters, limit=params.limit, derection=params.derection, cursor=params.parsed_cursor
    )
    return OrdersResponse.jsonify(
        items=list(result),
        limit=params.limit,
        next=base64_encode_json(result.last_evaluated_key),
        previous=params.cursor,
    )


@app.get("/orders/<order_id>")
@api_key_required
@inject
def get_order(user_id: str, order_id: str, order_service: OrderService):
    if order := order_service.get(user_id, order_id):
        return OrderResponse.jsonify(order)
    raise NotFoundError(order_id)


@app.post("/orders")
@api_key_required
@inject
def create_order(user_id: str, order_service: OrderService):
    data = OrderCreateRequest(**request.json).model_dump()
    order = order_service.create(user_id, data["address"], data["items"])
    return OrderResponse.jsonify(order), 201


@app.put("/orders/<order_id>")
@api_key_required
@inject
def cancel_order(user_id: str, order_id: str, order_service: OrderService):
    order_service.update(user_id, order_id, "CANCELED")
    return Response.jsonify(id=order_id)
