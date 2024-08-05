from pynamodb.models import ResultIterator
from werkzeug.security import check_password_hash, generate_password_hash

from app.adapters.repositories import UserRepository
from app.common.exceptions import AuthenticationError, ConflictError, NotFoundError
from app.db.models import UserModel
from app.utils.datetime_utils import timestamp_to_hex


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_by_id(self, user_id: str) -> UserModel:
        return self.user_repository.get(hash_key="USER", range_key=user_id)

    def get_by_email(self, email: str) -> UserModel:
        result = self.user_repository.query(
            hash_key="USER",
            range_key_condition=UserModel.sku == email,
            index=UserModel.lsi,
        )
        if user := next(result, None):
            return user
        raise NotFoundError(f"User with email {email} not found")

    def register(self, name: str, email: str, password: str) -> UserModel:
        # if email is already taken, raise Exception
        if self.user_repository.exist(email):
            raise ConflictError(f"Email {email} already exists")
        return self.user_repository.create(
            {
                "name": name,
                "email": email,
                "password": generate_password_hash(password),
            }
        )

    def login(self, email: str, password: str) -> UserModel:
        user = self.get_by_email(email)
        if check_password_hash(user.password, password):
            return user
        raise AuthenticationError("Invalid email or password, Please try again!")

    def update(self, user_id: str, attributes: dict):
        if password := attributes.get("password"):
            attributes["password"] = generate_password_hash(password)
        if email := attributes.get("email"):
            attributes["sku"] = email
        try:
            self.user_repository.update(hash_key="USER", range_key=user_id, attributes=attributes)
        except ConflictError:
            raise NotFoundError(f"User <{user_id}> not found")

    def delete(self, user_id: str):
        try:
            self.user_repository.delete(hash_key="USER", range_key=user_id, ignore_if_not_exist=False)
        except ConflictError:
            raise NotFoundError(f"User<{user_id}> not found")

    def list(
        self,
        filters: dict | None = None,
        derection: str = "asc",
        cursor: dict | None = None,
        limit: int = 50,
    ) -> ResultIterator[UserModel]:
        range_key_condition = filter_condition = None
        # set range_key_condition, filter by createdAt
        since = filters.get("since")
        until = filters.get("until")
        if since and until:
            range_key_condition = UserModel.sk.between(timestamp_to_hex(since), timestamp_to_hex(until))
        elif since:
            range_key_condition = UserModel.sk >= timestamp_to_hex(since)
        elif until:
            range_key_condition = UserModel.sk < timestamp_to_hex(until)
        # filter by name
        if name := filters.get("name"):
            filter_condition = UserModel.name.contains(name)
        return self.user_repository.query(
            hash_key="USER",
            range_key_condition=range_key_condition,
            last_evaluated_key=cursor,
            scan_index_forward="asc" == derection,
            filter_condition=filter_condition,
            limit=limit,
        )

    def list_by_email(
        self,
        email: str,
        filters: dict | None = None,
        derection: str = "asc",
        cursor: dict | None = None,
        limit: int = 50,
    ) -> ResultIterator[UserModel]:
        range_key_condition = UserModel.sku.startswith(email)
        # set filter_condition
        filter_condition = None
        if name := filters.get("name"):
            filter_condition &= UserModel.name.contains(name)
        since = filters.get("since")
        until = filters.get("until")
        if since and until:
            filter_condition &= UserModel.createdAt.between(timestamp_to_hex(since), timestamp_to_hex(until))
        elif since:
            filter_condition &= UserModel.createdAt >= timestamp_to_hex(since)
        elif until:
            filter_condition &= UserModel.createdAt < timestamp_to_hex(until)
        return self.user_repository.query(
            hash_key="USER",
            range_key_condition=range_key_condition,
            filter_condition=filter_condition,
            index=UserModel.lsi,
            scan_index_forward="asc" == derection,
            last_evaluated_key=cursor,
            limit=limit,
        )
