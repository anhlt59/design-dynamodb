from flask import Blueprint, request
from injector import inject

from app.adapters.presenters.base import Response
from app.adapters.presenters.categories import (
    CategoriesRequest,
    CategoriesResponse,
    CategoryCreateRequest,
    CategoryResponse,
    CategoryUpdateRequest,
)
from app.common.exceptions import NotFoundError
from app.framework.middlewares import api_key_required
from app.services import CategoryService
from app.utils.encode_utils import base64_encode_json

app = Blueprint("categories", __name__)


@app.get("")
@api_key_required
@inject
def list_categories(category_service: CategoryService):
    params = CategoriesRequest(**request.args)
    result = category_service.list(
        filters=params.filters, limit=params.limit, derection=params.derection, cursor=params.parsed_cursor
    )
    return CategoriesResponse.jsonify(
        items=list(result),
        limit=params.limit,
        next=base64_encode_json(result.last_evaluated_key),
        previous=params.cursor,
    )


@app.get("/<category_id>")
@api_key_required
@inject
def get_category(category_id: str, category_service: CategoryService):
    if category := category_service.get(category_id):
        return CategoryResponse.jsonify(category)
    raise NotFoundError(category_id)


@app.post("")
@api_key_required
@inject
def create_category(category_service: CategoryService):
    data = CategoryCreateRequest(**request.json)
    category = category_service.create(data.name)
    return CategoryResponse.jsonify(category), 201


@app.put("/<category_id>")
@api_key_required
@inject
def update_category(category_id: str, category_service: CategoryService):
    data = CategoryUpdateRequest(**request.json)
    category_service.update(category_id, data.name)
    return Response.jsonify(id=category_id)


@app.delete("/<category_id>")
@api_key_required
@inject
def delete_category(category_id: str, category_service: CategoryService):
    category_service.delete(category_id)
    return Response.jsonify(id=category_id)
