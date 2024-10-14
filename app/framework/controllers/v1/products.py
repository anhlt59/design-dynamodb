from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.adapters.presenters.products import (
    ProductCreateRequest,
    ProductResponse,
    ProductsRequest,
    ProductsResponse,
    ProductUpdateRequest,
)
from app.common.exceptions import NotFoundException
from app.framework.containers import Container
from app.services import ProductService

router = APIRouter(prefix="/products")


@router.get("", response_model=ProductsResponse)
@inject
def list_products(
    params: Annotated[ProductsRequest, Depends()],
    product_service: ProductService = Depends(Provide[Container.product_service]),
):
    filters = {
        "name": params.name,
        "categoryId": params.categoryId,
        "brandId": params.brandId,
        "priceGT": params.priceGT,
        "priceLT": params.priceLT,
        "since": params.since,
        "until": params.until,
    }
    if params.brandId:
        result = product_service.list_by_brand(
            params.brandId,
            filters=filters,
            limit=params.limit,
            direction=params.direction,
            cursor=params.cursor,
        )
    elif params.categoryId:
        result = product_service.list_by_category(
            params.categoryId,
            filters=filters,
            limit=params.limit,
            direction=params.direction,
            cursor=params.cursor,
        )
    else:
        result = product_service.list(
            filters=filters,
            limit=params.limit,
            direction=params.direction,
            cursor=params.cursor,
        )
    return {
        "items": list(result),
        "limit": params.limit,
        "next": result.last_evaluated_key,
        "previous": params.cursor,
    }


@router.get("/{product_id}", response_model=ProductResponse)
@inject
def get_product(product_id: str, product_service: ProductService = Depends(Provide[Container.product_service])):
    if product := product_service.get(product_id):
        return product
    raise NotFoundException(product_id)


@router.post("", status_code=201, response_model=None)
@inject
def create_product(
    payload: ProductCreateRequest, product_service: ProductService = Depends(Provide[Container.product_service])
):
    product = product_service.create(payload)
    return {"id": product.id}


@router.put("/{product_id}", response_model=None)
@inject
def update_product(
    product_id: str,
    payload: ProductUpdateRequest,
    product_service: ProductService = Depends(Provide[Container.product_service]),
):
    product_service.update(product_id, payload)
    return {"id": product_id}


@router.delete("/{product_id}", response_model=None)
@inject
def delete_product(product_id: str, product_service: ProductService = Depends(Provide[Container.product_service])):
    product_service.delete(product_id)
    return {"id": product_id}
