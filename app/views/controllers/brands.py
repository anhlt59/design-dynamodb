from flask import Blueprint, jsonify, request
from injector import inject

from app.core.exceptions import NotFoundError, ValidationError
from app.core.middlewares import api_key_required
from app.services import BrandService
from app.utils.encode_utils import base64_decode_json, base64_encode_json

app = Blueprint("api/v1/brands", __name__)


@app.route("", methods=["GET"])
@api_key_required
@inject
def list_brands(brand_service: BrandService):
    derection = request.args.get("derection", default="asc", type=str)
    limit = request.args.get("limit", default=20, type=int)
    base64_cusor = request.args.get("cursor", default=None, type=str)
    filters = {"name": request.args.get("name", default=None, type=str)}

    result = brand_service.list(
        filters=filters, limit=limit, derection=derection, cursor=base64_decode_json(base64_cusor)
    )
    return jsonify(
        {
            "items": list(result),
            "page": {"limit": limit, "next": base64_encode_json(result.last_evaluated_key), "previous": base64_cusor},
        }
    )


@app.route("/<brand_id>", methods=["GET"])
@api_key_required
@inject
def get_brand(brand_id: str, brand_service: BrandService):
    if brand := brand_service.get(brand_id):
        return jsonify(brand)
    raise NotFoundError(brand_id)


@app.route("", methods=["POST"])
@api_key_required
@inject
def create_brand(brand_service: BrandService):
    if name := request.json.get("name"):
        brand = brand_service.create(name)
        return jsonify({"id": brand.id}), 201
    raise ValidationError("Name is required")


@app.route("/<brand_id>", methods=["PUT"])
@api_key_required
@inject
def update_brand(brand_id: str, brand_service: BrandService):
    if name := request.json.get("name"):
        brand_service.update(brand_id, name)
        return jsonify({"id": brand_id})
    raise ValidationError("Name is required")


@app.route("/<brand_id>", methods=["DELETE"])
@api_key_required
@inject
def delete_brand(brand_id: str, brand_service: BrandService):
    brand_service.delete(brand_id)
    return jsonify({"id": brand_id})
