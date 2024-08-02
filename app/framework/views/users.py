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
from app.controllers import UserController
from app.core.exceptions import NotFoundError
from app.framework.middlewares import api_key_required
from app.utils.encode_utils import base64_encode_json

app = Blueprint("api/v1/users", __name__)


@app.route("", methods=["GET"])
@api_key_required
@inject
def list_users(user_controller: UserController):
    params = UsersRequest(**request.args)
    result = user_controller.list(
        filters=params.filters, limit=params.limit, derection=params.derection, cursor=params.parsed_cursor
    )
    return UsersResponse.jsonify(
        items=list(result),
        limit=params.limit,
        next=base64_encode_json(result.last_evaluated_key),
        previous=params.cursor,
    )


@app.route("/<user_id>", methods=["GET"])
@api_key_required
@inject
def get_user(user_id: str, user_controller: UserController):
    if user := user_controller.get_by_id(user_id):
        return UserResponse.jsonify(user)
    raise NotFoundError(user_id)


@app.route("", methods=["POST"])
@api_key_required
@inject
def register_user(user_controller: UserController):
    data = UserCreateRequest(**request.json)
    user = user_controller.register(data.name, data.email, data.password)
    return UserResponse.jsonify(user), 201


@app.route("/<user_id>", methods=["PUT"])
@api_key_required
@inject
def update_user(user_id: str, user_controller: UserController):
    data = UserUpdateRequest(**request.json)
    user_controller.update(user_id, data.dict())
    return Response.jsonify(id=user_id)


@app.route("/<user_id>", methods=["DELETE"])
@api_key_required
@inject
def delete_user(user_id: str, user_controller: UserController):
    user_controller.delete(user_id)
    return Response.jsonify(id=user_id)
