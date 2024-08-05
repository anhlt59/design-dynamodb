from flask import Blueprint, request
from injector import inject

from app.adapters.presenters.base import Response
from app.adapters.presenters.brands import (
    BrandCreateRequest,
    BrandResponse,
    BrandsRequest,
    BrandsResponse,
    BrandUpdateRequest,
)
from app.controllers import BrandController
from app.core.exceptions import NotFoundError
from app.framework.middlewares import api_key_required
from app.utils.encode_utils import base64_encode_json

app = Blueprint("api/v1/brands", __name__)


@app.route("", methods=["GET"])
@api_key_required
@inject
def list_brands(brand_controller: BrandController):
    params = BrandsRequest(**request.args)
    result = brand_controller.list(
        filters=params.filters, limit=params.limit, derection=params.derection, cursor=params.parsed_cursor
    )
    return BrandsResponse.jsonify(
        items=list(result),
        limit=params.limit,
        next=base64_encode_json(result.last_evaluated_key),
        previous=params.cursor,
    )


@app.route("/<brand_id>", methods=["GET"])
@api_key_required
@inject
def get_brand(brand_id: str, brand_controller: BrandController):
    if brand := brand_controller.get(brand_id):
        return BrandResponse.jsonify(brand)
    raise NotFoundError(brand_id)


@app.route("", methods=["POST"])
@api_key_required
@inject
def create_brand(brand_controller: BrandController):
    data = BrandCreateRequest(**request.json)
    brand = brand_controller.create(data.name)
    return BrandResponse.jsonify(brand), 201


@app.route("/<brand_id>", methods=["PUT"])
@api_key_required
@inject
def update_brand(brand_id: str, brand_controller: BrandController):
    data = BrandUpdateRequest(**request.json)
    brand_controller.update(brand_id, data.name)
    return Response.jsonify(id=brand_id)


@app.route("/<brand_id>", methods=["DELETE"])
@api_key_required
@inject
def delete_brand(brand_id: str, brand_controller: BrandController):
    brand_controller.delete(brand_id)
    return Response.jsonify(id=brand_id)
