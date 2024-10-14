from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.adapters.presenters.users import (
    UserCreateRequest,
    UserResponse,
    UsersRequest,
    UsersResponse,
    UserUpdateRequest,
)
from app.common.exceptions import NotFoundException
from app.framework.containers import Container
from app.services import UserService

router = APIRouter(prefix="/users")


@router.get("", response_model=UsersResponse)
@inject
def list_users(
    params: Annotated[UsersRequest, Depends()], user_service: UserService = Depends(Provide[Container.user_service])
):
    result = user_service.list(
        filters={"name": params.name, "since": params.since, "until": params.until},
        limit=params.limit,
        direction=params.direction,
        cursor=params.cursor,
    )
    return {"items": list(result), "limit": params.limit, "next": result.last_evaluated_key, "previous": params.cursor}


@router.get("/{user_id}", response_model=UserResponse)
@inject
def get_user(user_id: str, user_service: UserService = Depends(Provide[Container.user_service])):
    if user := user_service.get_by_id(user_id):
        return user
    raise NotFoundException(user_id)


@router.post("", status_code=201, response_model=None)
@inject
def register_user(payload: UserCreateRequest, user_service: UserService = Depends(Provide[Container.user_service])):
    user = user_service.register(payload.name, payload.email, payload.password)
    return {"id": user.id}


@router.put("/{user_id}", response_model=None)
@inject
def update_user(
    user_id: str, payload: UserUpdateRequest, user_service: UserService = Depends(Provide[Container.user_service])
):
    user_service.update(user_id, payload)
    return {"id": user_id}


@router.delete("/{user_id}", response_model=None)
@inject
def delete_user(user_id: str, user_service: UserService = Depends(Provide[Container.user_service])):
    user_service.delete(user_id)
    return {"id": user_id}
