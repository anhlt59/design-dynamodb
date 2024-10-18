from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.adapters.api.containers import Container
from app.domain.models import (
    CreateUserInputDto,
    PaginatedOutputDTO,
    PaginatedUserInputDto,
    UpdateUserInputDto,
    UserOutputDto,
)
from app.domain.ports.use_cases import IUserUseCase

router = APIRouter(prefix="/users")


@router.get("", response_model=PaginatedOutputDTO[UserOutputDto])
@inject
def list_users(
    params: Annotated[PaginatedUserInputDto, Depends()],
    user_use_case: IUserUseCase = Depends(Provide[Container.user_use_case]),
):
    return user_use_case.list(params)


@router.get("/{user_id}", response_model=UserOutputDto)
@inject
def get_user(
    user_id: str,
    user_use_case: IUserUseCase = Depends(Provide[Container.user_use_case]),
):
    return user_use_case.get_by_id(user_id)


@router.post("", status_code=201, response_model=None)
@inject
def register_user(
    payload: CreateUserInputDto,
    user_use_case: IUserUseCase = Depends(Provide[Container.user_use_case]),
):
    user = user_use_case.register(payload)
    return {"id": user.id}


@router.put("/{user_id}", response_model=None)
@inject
def update_user(
    user_id: str,
    payload: UpdateUserInputDto,
    user_use_case: IUserUseCase = Depends(Provide[Container.user_use_case]),
):
    user_use_case.update(user_id, payload)
    return {"id": user_id}


@router.delete("/{user_id}", response_model=None)
@inject
def delete_user(
    user_id: str,
    user_use_case: IUserUseCase = Depends(Provide[Container.user_use_case]),
):
    user_use_case.delete(user_id)
    return {"id": user_id}
