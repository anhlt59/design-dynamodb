from flask import Blueprint, request
from injector import inject

from app.adapters.presenters.base import Response
from app.adapters.presenters.products import (
    ProductCreateRequest,
    ProductResponse,
    ProductsRequest,
    ProductsResponse,
    ProductUpdateRequest,
)
from app.controllers import ProductController
from app.core.exceptions import NotFoundError
from app.framework.middlewares import api_key_required
from app.utils.encode_utils import base64_encode_json

app = Blueprint("products", __name__)


@app.get("")
@api_key_required
@inject
def list_products(product_controller: ProductController):
    params = ProductsRequest(**request.args)
    if params.brandId:
        result = product_controller.list_by_brand(
            params.brandId,
            filters=params.filters,
            limit=params.limit,
            derection=params.derection,
            cursor=params.parsed_cursor,
        )
    elif params.categoryId:
        result = product_controller.list_by_category(
            params.categoryId,
            filters=params.filters,
            limit=params.limit,
            derection=params.derection,
            cursor=params.parsed_cursor,
        )
    else:
        result = product_controller.list(
            filters=params.filters, limit=params.limit, derection=params.derection, cursor=params.parsed_cursor
        )
    return ProductsResponse.jsonify(
        items=list(result),
        limit=params.limit,
        next=base64_encode_json(result.last_evaluated_key),
        previous=params.cursor,
    )


@app.get("/<product_id>")
@api_key_required
@inject
def get_product(product_id: str, product_controller: ProductController):
    if product := product_controller.get(product_id):
        return ProductResponse.jsonify(product)
    raise NotFoundError(product_id)


@app.post("")
@api_key_required
@inject
def create_product(product_controller: ProductController):
    data = ProductCreateRequest(**request.json).model_dump()
    product = product_controller.create(data)
    return ProductResponse.jsonify(product), 201


@app.put("/<product_id>")
@api_key_required
@inject
def update_product(product_id: str, product_controller: ProductController):
    data = ProductUpdateRequest(**request.json).model_dump()
    product_controller.update(product_id, data)
    return Response.jsonify(id=product_id)


@app.delete("/<product_id>")
@api_key_required
@inject
def delete_product(product_id: str, product_controller: ProductController):
    product_controller.delete(product_id)
    return Response.jsonify(id=product_id)
