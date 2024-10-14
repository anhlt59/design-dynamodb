from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.adapters.presenters.brands import (
    BrandCreateRequest,
    BrandResponse,
    BrandsRequest,
    BrandsResponse,
    BrandUpdateRequest,
)
from app.common.exceptions import NotFoundException
from app.framework.containers import Container
from app.services import BrandService

router = APIRouter(prefix="/brands")


@router.get("", response_model=BrandsResponse)
@inject
def list_brands(
    params: Annotated[BrandsRequest, Depends()],
    brand_service: BrandService = Depends(Provide[Container.brand_service]),
):
    result = brand_service.list(
        filters={"name": params.name}, limit=params.limit, direction=params.direction, cursor=params.cursor
    )
    return {
        "items": list(result),
        "limit": params.limit,
        "next": result.last_evaluated_key,
        "previous": params.cursor,
    }


@router.get("/{brand_id}", response_model=BrandResponse)
@inject
def get_brand(brand_id: str, brand_service: BrandService = Depends(Provide[Container.brand_service])):
    if brand := brand_service.get(brand_id):
        return brand
    raise NotFoundException(brand_id)


@router.post("", status_code=201, response_model=None)
@inject
def create_brand(payload: BrandCreateRequest, brand_service: BrandService = Depends(Provide[Container.brand_service])):
    brand = brand_service.create(payload.name)
    return {"id": brand.id}


@router.put("/{brand_id}", response_model=None)
@inject
def update_brand(
    brand_id: str, payload: BrandUpdateRequest, brand_service: BrandService = Depends(Provide[Container.brand_service])
):
    brand_service.update(brand_id, payload.name)
    return {"id": brand_id}


@router.delete("/{brand_id}", response_model=None)
@inject
def delete_brand(brand_id: str, brand_service: BrandService = Depends(Provide[Container.brand_service])):
    brand_service.delete(brand_id)
    return {"id": brand_id}
