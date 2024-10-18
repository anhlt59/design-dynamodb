from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.adapters.api.containers import Container
from app.domain.models import (
    BrandOutputDto,
    CreateBrandInputDto,
    PaginatedBrandInputDto,
    PaginatedOutputDTO,
    UpdateBrandInputDto,
)
from app.domain.ports.use_cases import IBrandUseCase

router = APIRouter(prefix="/brands")


@router.get("", response_model=PaginatedOutputDTO[BrandOutputDto])
@inject
def list_brands(
    params: Annotated[PaginatedBrandInputDto, Depends()],
    brand_use_case: IBrandUseCase = Depends(Provide[Container.brand_use_case]),
):
    return brand_use_case.list(params)


@router.get("/{brand_id}", response_model=BrandOutputDto)
@inject
def get_brand(
    brand_id: str,
    brand_use_case: IBrandUseCase = Depends(Provide[Container.brand_use_case]),
):
    return brand_use_case.get(brand_id)


@router.post("", status_code=201, response_model=None)
@inject
def create_brand(
    payload: CreateBrandInputDto,
    brand_use_case: IBrandUseCase = Depends(Provide[Container.brand_use_case]),
):
    brand = brand_use_case.create(payload)
    return {"id": brand.id}


@router.put("/{brand_id}", response_model=None)
@inject
def update_brand(
    brand_id: str,
    payload: UpdateBrandInputDto,
    brand_use_case: IBrandUseCase = Depends(Provide[Container.brand_use_case]),
):
    brand_use_case.update(brand_id, payload)
    return {"id": brand_id}


@router.delete("/{brand_id}", response_model=None)
@inject
def delete_brand(
    brand_id: str,
    brand_use_case: IBrandUseCase = Depends(Provide[Container.brand_use_case]),
):
    brand_use_case.delete(brand_id)
    return {"id": brand_id}
