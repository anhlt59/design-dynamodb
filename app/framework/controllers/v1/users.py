from flask import Blueprint, request
from injector import inject

from app.adapters.presenters.base import Response
from app.adapters.presenters.users import (
    UserCreateRequest,
    UserResponse,
    UsersRequest,
    UsersResponse,
    UserUpdateRequest,
)
from app.common.exceptions import NotFoundError
from app.framework.middlewares import api_key_required
from app.services import UserService
from app.utils.encode_utils import base64_encode_json

app = Blueprint("users", __name__)


@app.get("")
@api_key_required
@inject
def list_users(user_service: UserService):
    params = UsersRequest(**request.args)
    result = user_service.list(
        filters=params.filters, limit=params.limit, derection=params.derection, cursor=params.parsed_cursor
    )
    return UsersResponse.jsonify(
        items=list(result),
        limit=params.limit,
        next=base64_encode_json(result.last_evaluated_key),
        previous=params.cursor,
    )


@app.get("/<user_id>")
@api_key_required
@inject
def get_user(user_id: str, user_service: UserService):
    if user := user_service.get_by_id(user_id):
        return UserResponse.jsonify(user)
    raise NotFoundError(user_id)


@app.post("")
@api_key_required
@inject
def register_user(user_service: UserService):
    data = UserCreateRequest(**request.json)
    user = user_service.register(data.name, data.email, data.password)
    return UserResponse.jsonify(user), 201


@app.put("/<user_id>")
@api_key_required
@inject
def update_user(user_id: str, user_service: UserService):
    data = UserUpdateRequest(**request.json)
    user_service.update(user_id, data.model_dump())
    return Response.jsonify(id=user_id)


@app.delete("/<user_id>")
@api_key_required
@inject
def delete_user(user_id: str, user_service: UserService):
    user_service.delete(user_id)
    return Response.jsonify(id=user_id)
