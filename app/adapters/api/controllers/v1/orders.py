from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.adapters.api.containers import Container
from app.domain.models import CreateOrderInputDto, OrderOutputDto, PaginatedOrderInputDto, PaginatedOutputDTO
from app.domain.ports.use_cases import IOrderUseCase

router = APIRouter(prefix="/users/{user_id}/orders")


@router.get("", response_model=PaginatedOutputDTO[OrderOutputDto])
@inject
def list_user_orders(
    user_id: str,
    params: Annotated[PaginatedOrderInputDto, Depends()],
    order_use_case: IOrderUseCase = Depends(Provide[Container.order_use_case]),
):
    return order_use_case.list_user_orders(user_id, params)


@router.get("/{order_id}", response_model=OrderOutputDto)
@inject
def get_order(
    user_id: str,
    order_id: str,
    order_use_case: IOrderUseCase = Depends(Provide[Container.order_use_case]),
):
    return order_use_case.get(user_id, order_id)


@router.post("", status_code=201, response_model=None)
@inject
def create_order(
    user_id: str,
    payload: CreateOrderInputDto,
    order_use_case: IOrderUseCase = Depends(Provide[Container.order_use_case]),
):
    order = order_use_case.create(user_id, payload)
    return {"id": order.id}


@router.put("/{order_id}", response_model=None)
@inject
def cancel_order(
    user_id: str,
    order_id: str,
    order_use_case: IOrderUseCase = Depends(Provide[Container.order_use_case]),
):
    order_use_case.cancel(user_id, order_id)
    return {"id": order_id}
