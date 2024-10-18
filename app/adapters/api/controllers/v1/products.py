from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.adapters.api.containers import Container
from app.domain.models import (
    CreateProductInputDto,
    PaginatedOutputDTO,
    PaginatedProductInputDto,
    ProductOutputDto,
    UpdateProductInputDto,
)
from app.domain.ports.use_cases import IProductUseCase

router = APIRouter(prefix="/products")


@router.get("", response_model=PaginatedOutputDTO[ProductOutputDto])
@inject
def list_products(
    params: Annotated[PaginatedProductInputDto, Depends()],
    product_use_case: IProductUseCase = Depends(Provide[Container.product_use_case]),
):
    return product_use_case.list(params)


@router.get("/{product_id}", response_model=ProductOutputDto)
@inject
def get_product(
    product_id: str,
    product_use_case: IProductUseCase = Depends(Provide[Container.product_use_case]),
):
    return product_use_case.get(product_id)


@router.post("", status_code=201, response_model=None)
@inject
def create_product(
    payload: CreateProductInputDto,
    product_use_case: IProductUseCase = Depends(Provide[Container.product_use_case]),
):
    product = product_use_case.create(payload)
    return {"id": product.id}


@router.put("/{product_id}", response_model=None)
@inject
def update_product(
    product_id: str,
    payload: UpdateProductInputDto,
    product_use_case: IProductUseCase = Depends(Provide[Container.product_use_case]),
):
    product_use_case.update(product_id, payload)
    return {"id": product_id}


@router.delete("/{product_id}", response_model=None)
@inject
def delete_product(
    product_id: str,
    product_use_case: IProductUseCase = Depends(Provide[Container.product_use_case]),
):
    product_use_case.delete(product_id)
    return {"id": product_id}
