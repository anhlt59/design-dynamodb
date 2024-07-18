from flask import Blueprint, jsonify, request
from injector import inject

from app.core.exceptions import NotFoundError
from app.core.middlewares import api_key_required
from app.services import ProductService
from app.utils.encode_utils import base64_decode_json, base64_encode_json

app = Blueprint("api/v1/products", __name__)


@app.route("", methods=["GET"])
@api_key_required
@inject
def list_products(product_service: ProductService):
    derection = request.args.get("derection", default="asc", type=str)
    limit = request.args.get("limit", default=20, type=int)
    base64_cusor = request.args.get("cursor", default=None, type=str)
    cursor = base64_decode_json(base64_cusor)
    filters = {
        "name": request.args.get("name", default=None, type=str),
        "priceGT": request.args.get("priceGT", default=None, type=int),
        "priceLT": request.args.get("priceLT", default=None, type=int),
        "since": request.args.get("since", default=None, type=int),
        "until": request.args.get("until", default=None, type=int),
        "brand_id": request.args.get("brandId", default=None, type=str),
        "category_id": request.args.get("categoryId", default=None, type=str),
    }
    if filters["brand_id"]:
        result = product_service.list_by_brand(
            filters["brand_id"], filters=filters, limit=limit, derection=derection, cursor=cursor
        )
    elif filters["category_id"]:
        result = product_service.list_by_category(
            filters["category_id"], filters=filters, limit=limit, derection=derection, cursor=cursor
        )
    else:
        result = product_service.list(filters=filters, limit=limit, derection=derection, cursor=cursor)
    return jsonify(
        {
            "items": list(result),
            "page": {"limit": limit, "next": base64_encode_json(result.last_evaluated_key), "previous": base64_cusor},
        }
    )


@app.route("/<product_id>", methods=["GET"])
@api_key_required
@inject
def get_product(product_id: str, product_service: ProductService):
    if product := product_service.get(product_id):
        return jsonify(product)
    raise NotFoundError(product_id)


@app.route("", methods=["POST"])
@api_key_required
@inject
def create_product(product_service: ProductService):
    params = {
        "name": request.json.get("name"),
        "price": request.json.get("price"),
        "stock": request.json.get("stock"),
        "categoryId": request.json.get("categoryId"),
        "brandId": request.json.get("brandId"),
    }
    product = product_service.create(params)
    return jsonify({"id": product.id}), 201


@app.route("/<product_id>", methods=["PUT"])
@api_key_required
@inject
def update_product(product_id: str, product_service: ProductService):
    params = {
        "name": request.json.get("name"),
        "price": request.json.get("price"),
        "stock": request.json.get("stock"),
        "categoryId": request.json.get("categoryId"),
        "brandId": request.json.get("brandId"),
    }
    product_service.update(product_id, params)
    return jsonify({"id": product_id})


@app.route("/<product_id>", methods=["DELETE"])
@api_key_required
@inject
def delete_product(product_id: str, product_service: ProductService):
    product_service.delete(product_id)
    return jsonify({"id": product_id})
