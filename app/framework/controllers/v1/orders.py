from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.adapters.presenters.orders import OrderCreateRequest, OrderResponse, OrdersRequest, OrdersResponse
from app.common.exceptions import NotFoundException
from app.framework.containers import Container
from app.services import OrderService

router = APIRouter(prefix="/users/{user_id}/orders")


@router.get("", response_model=OrdersResponse)
@inject
def list_user_orders(
    user_id: str,
    params: Annotated[OrdersRequest, Depends()],
    order_service: OrderService = Depends(Provide[Container.order_service]),
):
    result = order_service.list_orders_by_user(
        user_id,
        filters={"status": params.status, "since": params.since, "until": params.until},
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


@router.get("/{order_id}", response_model=OrderResponse)
@inject
def get_order(user_id: str, order_id: str, order_service: OrderService = Depends(Provide[Container.order_service])):
    if order := order_service.get(user_id, order_id):
        return order
    raise NotFoundException(order_id)


@router.post("", status_code=201, response_model=None)
@inject
def create_order(
    user_id: str, payload: OrderCreateRequest, order_service: OrderService = Depends(Provide[Container.order_service])
):
    order = order_service.create(user_id, payload.address, payload.items)
    return {"id": order.id}


@router.put("/{order_id}", response_model=None)
@inject
def cancel_order(user_id: str, order_id: str, order_service: OrderService = Depends(Provide[Container.order_service])):
    order_service.update(user_id, order_id, "CANCELED")
    return {"id": order_id}
