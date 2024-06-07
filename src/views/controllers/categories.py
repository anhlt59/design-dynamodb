from flask import Blueprint, jsonify, request
from injector import inject

from src.exceptions import NotFoundError, ValidationError
from src.middlewares import api_key_required
from src.services import CategoryService
from src.utils.encode_utils import base64_decode_json, base64_encode_json

app = Blueprint("api/v1/categories", __name__)


@app.route("", methods=["GET"])
@api_key_required
@inject
def list_categories(category_service: CategoryService):
    derection = request.args.get("derection", default="asc", type=str)
    limit = request.args.get("limit", default=20, type=int)
    base64_cusor = request.args.get("cursor", default=None, type=str)
    filters = {"name": request.args.get("name", default=None, type=str)}

    result = category_service.list(
        filters=filters, limit=limit, derection=derection, cursor=base64_decode_json(base64_cusor)
    )
    return jsonify(
        {
            "items": list(result),
            "page": {"limit": limit, "next": base64_encode_json(result.last_evaluated_key), "previous": base64_cusor},
        }
    )


@app.route("/<category_id>", methods=["GET"])
@api_key_required
@inject
def get_category(category_id: str, category_service: CategoryService):
    if category := category_service.get(category_id):
        return jsonify(category)
    raise NotFoundError(category_id)


@app.route("", methods=["POST"])
@api_key_required
@inject
def create_category(category_service: CategoryService):
    if name := request.json.get("name"):
        category = category_service.create(name)
        return jsonify({"id": category.id}), 201
    raise ValidationError("Name is required")


@app.route("/<category_id>", methods=["PUT"])
@api_key_required
@inject
def update_category(category_id: str, category_service: CategoryService):
    if name := request.json.get("name"):
        category_service.update(category_id, name)
        return jsonify({"id": category_id})
    raise ValidationError("Name is required")


@app.route("/<category_id>", methods=["DELETE"])
@api_key_required
@inject
def delete_category(category_id: str, category_service: CategoryService):
    category_service.delete(category_id)
    return jsonify({"id": category_id})
