from pynamodb.exceptions import TransactWriteError
from pynamodb.models import ResultIterator

from app.adapters.presenters.orders import OrderItem
from app.adapters.repositories import OrderRepository, ProductRepository
from app.common.exceptions import ConflictException, NotFoundException, UnprocessableEntityException
from app.db.models import OrderModel, ProductModel
from app.db.models.orders import OrderStatus
from app.utils.datetime_utils import timestamp_to_hex


class OrderService:
    def __init__(self, order_repository: OrderRepository, product_repository: ProductRepository):
        self.product_repository = product_repository
        self.order_repository = order_repository

    def get(self, user_id: str, order_id: str) -> OrderModel:
        return self.order_repository.get(hash_key=user_id, range_key=order_id)

    def create(self, user_id: str, address: str, items: list[OrderItem]) -> OrderModel:
        try:
            with self.order_repository.transaction() as transaction:
                # decrease stock of product
                total_price = 0
                for item in items:
                    total_price += item.price * item.quantity
                    transaction.update(
                        ProductModel(id=item.productId),
                        actions=[ProductModel.stock.set(ProductModel.stock - item.quantity)],
                        condition=(ProductModel.stock >= item.quantity),
                    )
                # create order
                order = OrderModel(
                    userId=user_id,
                    items=[i.model_dump() for i in items],
                    totalPrice=total_price,
                    address=address,
                )
                transaction.save(order)
            return order
        except TransactWriteError as transaction_err:
            error_msgs = []
            for index, error in enumerate(transaction_err.cancellation_reasons[1:]):
                if error is not None:
                    error_msgs.append(f"Product<{items[index].productId}> is out of stock")
            raise UnprocessableEntityException(", ".join(error_msgs))
        except Exception as e:
            print(e)

    def update(self, user_id: str, order_id: str, status: str):
        try:
            self.order_repository.update(hash_key=user_id, range_key=order_id, attributes={"status": status})
        except ConflictException:
            raise NotFoundException(f"Order<{order_id}> not found")

    def delete(self, user_id: str, order_id: str):
        try:
            self.order_repository.delete(hash_key=user_id, range_key=order_id)
        except ConflictException:
            raise NotFoundException(f"Order<{order_id}> not found")

    def list_orders_by_user(
        self,
        user_id: str,
        filters: dict | None = None,
        direction: str = "asc",
        cursor: dict | None = None,
        limit: int = 50,
    ) -> ResultIterator[OrderModel]:
        range_key_condition = filter_condition = None

        if filters is not None:
            # filter by createdAt
            since = filters.get("since")
            until = filters.get("until")
            if since and until:
                range_key_condition = OrderModel.sk.between(timestamp_to_hex(since), timestamp_to_hex(until))
            elif since:
                range_key_condition = OrderModel.sk >= timestamp_to_hex(since)
            elif until:
                range_key_condition = OrderModel.sk < timestamp_to_hex(until)
            else:
                range_key_condition = OrderModel.sk.startswith("")
            # filter_condition by status
            if status := filters.get("status"):
                filter_condition = OrderModel.status == status

        return self.order_repository.query(
            hash_key=user_id,
            range_key_condition=range_key_condition,
            filter_condition=filter_condition,
            scan_index_forward="asc" == direction,
            last_evaluated_key=cursor,
            limit=limit,
        )

    def list_orders_by_status(
        self,
        status: OrderStatus,
        filters: dict | None = None,
        direction: str = "asc",
        cursor: dict | None = None,
        limit: int = 50,
    ) -> ResultIterator[OrderModel]:
        # filter by updatedAt
        since = filters.get("since")
        until = filters.get("until")
        if since and until:
            range_key_condition = OrderModel.sk.between(timestamp_to_hex(since), timestamp_to_hex(until))
        elif since:
            range_key_condition = OrderModel.sk >= timestamp_to_hex(since)
        elif until:
            range_key_condition = OrderModel.sk < timestamp_to_hex(until)
        else:
            range_key_condition = None
        return self.order_repository.query(
            hash_key=status,
            range_key_condition=range_key_condition,
            index=OrderModel.gsi1,
            scan_index_forward="asc" == direction,
            last_evaluated_key=cursor,
            limit=limit,
        )
