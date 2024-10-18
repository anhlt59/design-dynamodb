from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.adapters.api.containers import Container
from app.domain.models import (
    CategoryOutputDto,
    CreateCategoryInputDto,
    PaginatedCategoryInputDto,
    PaginatedOutputDTO,
    UpdateCategoryInputDto,
)
from app.domain.ports.use_cases import ICategoryUseCase

router = APIRouter(prefix="/categories")


@router.get("", response_model=PaginatedOutputDTO[CategoryOutputDto])
@inject
def list_categories(
    params: Annotated[PaginatedCategoryInputDto, Depends()],
    category_use_case: ICategoryUseCase = Depends(Provide[Container.category_use_case]),
):
    return category_use_case.list(params)


@router.get("/{category_id}", response_model=CategoryOutputDto)
@inject
def get_category(
    category_id: str,
    category_use_case: ICategoryUseCase = Depends(Provide[Container.category_use_case]),
):
    return category_use_case.get(category_id)


@router.post("", status_code=201, response_model=None)
@inject
def create_category(
    payload: CreateCategoryInputDto,
    category_use_case: ICategoryUseCase = Depends(Provide[Container.category_use_case]),
):
    category = category_use_case.create(payload)
    return {"id": category.id}


@router.put("/{category_id}", response_model=None)
@inject
def update_category(
    category_id: str,
    payload: UpdateCategoryInputDto,
    category_use_case: ICategoryUseCase = Depends(Provide[Container.category_use_case]),
):
    category_use_case.update(category_id, payload)
    return {"id": category_id}


@router.delete("/{category_id}", response_model=None)
@inject
def delete_category(
    category_id: str,
    category_use_case: ICategoryUseCase = Depends(Provide[Container.category_use_case]),
):
    category_use_case.delete(category_id)
    return {"id": category_id}
