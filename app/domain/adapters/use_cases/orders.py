from app.common.enums import OrderStatus
from app.common.exceptions.http import NotFoundException
from app.domain.models import CreateOrderInputDto, Order, PaginatedOrderInputDto, PaginatedOutputDTO
from app.domain.ports.unit_of_works import IOrderUnitOfWork


class OrderUseCase:
    def __init__(self, uow: IOrderUnitOfWork):
        self.uow = uow

    def get(self, user_id: str, order_id: str) -> Order:
        with self.uow:
            if order := self.uow.orders.get(user_id=user_id, order_id=order_id):
                return order
            raise NotFoundException(f"Order<id={order_id}> not found")

    def create(self, user_id: str, dto: CreateOrderInputDto) -> Order:
        order = Order(userId=user_id, items=dto.items, address=dto.address)
        with self.uow:
            # degrade stock, if any item is out of stock, raise exception
            for item in dto.items:
                self.uow.products.decrease_stock(item.productId, item.quantity)
            # create order
            self.uow.orders.create(order)
            self.uow.commit()
            return order

    def cancel(self, user_id: str, order_id: str):
        with self.uow:
            self.uow.orders.update(user_id, order_id, {"status": OrderStatus.CANCELLED})
            self.uow.commit()

    def delete(self, user_id: str, order_id: str):
        with self.uow:
            self.uow.orders.delete(user_id, order_id)
            self.uow.commit()

    def list_user_orders(self, user_id: str, dto: PaginatedOrderInputDto) -> PaginatedOutputDTO[Order]:
        with self.uow:
            return self.uow.orders.list(
                user_id=user_id,
                filters={"status": dto.status, "since": dto.since, "until": dto.until},
                direction=dto.direction,
                cursor=dto.cursor,
                limit=dto.limit,
            )
