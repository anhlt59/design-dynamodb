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
from app.common.exceptions import NotFoundError
from app.framework.middlewares import api_key_required
from app.services import BrandService
from app.utils.encode_utils import base64_encode_json

app = Blueprint("brands", __name__)


@app.get("")
@api_key_required
@inject
def list_brands(brand_service: BrandService):
    params = BrandsRequest(**request.args)
    result = brand_service.list(
        filters=params.filters, limit=params.limit, derection=params.derection, cursor=params.parsed_cursor
    )
    return BrandsResponse.jsonify(
        items=list(result),
        limit=params.limit,
        next=base64_encode_json(result.last_evaluated_key),
        previous=params.cursor,
    )


@app.get("/<brand_id>")
@api_key_required
@inject
def get_brand(brand_id: str, brand_service: BrandService):
    if brand := brand_service.get(brand_id):
        return BrandResponse.jsonify(brand)
    raise NotFoundError(brand_id)


@app.post("")
@api_key_required
@inject
def create_brand(brand_service: BrandService):
    data = BrandCreateRequest(**request.json)
    brand = brand_service.create(data.name)
    return BrandResponse.jsonify(brand), 201


@app.put("/<brand_id>")
@api_key_required
@inject
def update_brand(brand_id: str, brand_service: BrandService):
    data = BrandUpdateRequest(**request.json)
    brand_service.update(brand_id, data.name)
    return Response.jsonify(id=brand_id)


@app.delete("/<brand_id>")
@api_key_required
@inject
def delete_brand(brand_id: str, brand_service: BrandService):
    brand_service.delete(brand_id)
    return Response.jsonify(id=brand_id)
