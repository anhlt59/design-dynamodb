from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.adapters.presenters.categories import (
    CategoriesRequest,
    CategoriesResponse,
    CategoryCreateRequest,
    CategoryResponse,
    CategoryUpdateRequest,
)
from app.common.exceptions import NotFoundException
from app.framework.containers import Container
from app.services import CategoryService

router = APIRouter(prefix="/categories")


@router.get("", response_model=CategoriesResponse)
@inject
def list_categories(
    params: Annotated[CategoriesRequest, Depends()],
    category_service: CategoryService = Depends(Provide[Container.category_service]),
):
    result = category_service.list(
        filters={"name": params.name}, limit=params.limit, direction=params.direction, cursor=params.cursor
    )
    return {
        "items": list(result),
        "limit": params.limit,
        "next": result.last_evaluated_key,
        "previous": params.cursor,
    }


@router.get("/{category_id}", response_model=CategoryResponse)
@inject
def get_category(category_id: str, category_service: CategoryService = Depends(Provide[Container.category_service])):
    if category := category_service.get(category_id):
        return category
    raise NotFoundException(category_id)


@router.post("", status_code=201, response_model=None)
@inject
def create_category(
    payload: CategoryCreateRequest,
    category_service: CategoryService = Depends(Provide[Container.category_service]),
):
    category = category_service.create(payload.name)
    return {"id": category.id}


@router.put("/{category_id}", response_model=None)
@inject
def update_category(
    category_id: str,
    payload: CategoryUpdateRequest,
    category_service: CategoryService = Depends(Provide[Container.category_service]),
):
    category_service.update(category_id, payload.name)
    return {"id": category_id}


@router.delete("/{category_id}", response_model=None)
@inject
def delete_category(
    category_id: str, category_service: CategoryService = Depends(Provide[Container.category_service])
):
    category_service.delete(category_id)
    return {"id": category_id}
