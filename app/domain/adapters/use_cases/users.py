from werkzeug.security import check_password_hash, generate_password_hash

from app.common.exceptions.http import ConflictException, NotFoundException, UnauthorizedException
from app.domain.models import CreateUserInputDto, PaginatedOutputDTO, PaginatedUserInputDto, UpdateUserInputDto, User
from app.domain.ports.unit_of_works import IUserUnitOfWork


class UserUseCase:
    def __init__(self, uow: IUserUnitOfWork):
        self.uow = uow

    def get_by_id(self, id: str) -> User:
        with self.uow:
            if user := self.uow.users.get_by_id(id):
                return user
            raise NotFoundException(f"User<id={id}> not found")

    def get_by_email(self, email: str) -> User:
        with self.uow:
            if user := self.uow.users.get_by_email(email):
                return user
            raise NotFoundException(f"User<email={email}> not found")

    def list(self, dto: PaginatedUserInputDto) -> PaginatedOutputDTO[User]:
        with self.uow:
            return self.uow.users.list(
                filters={"name": dto.name, "since": dto.since, "until": dto.until},
                limit=dto.limit,
                direction=dto.direction,
                cursor=dto.cursor,
            )

    def login(self, email: str, password: str) -> User:
        with self.uow:
            user = self.get_by_email(email)
            if check_password_hash(user.password, password):
                return user
            raise UnauthorizedException("Invalid email or password")

    def register(self, dto: CreateUserInputDto):
        user = User.model_validate(dto)
        with self.uow:
            # if email is already taken, raise Exception
            if self.uow.users.count_by_email(user.email):
                raise ConflictException(f"Email {user.email} already exists")
            # hash password
            user.password = generate_password_hash(user.password)
            self.uow.users.create(user)
            self.uow.commit()
        return user

    def update(self, id: str, dto: UpdateUserInputDto):
        with self.uow:
            attributes = dto.model_dump(exclude_none=True)
            if password := dto.password:
                attributes["password"] = generate_password_hash(password)
            self.uow.users.update(id, attributes=attributes)
            self.uow.commit()

    def delete(self, id: str):
        with self.uow:
            self.uow.users.delete(id)
            self.uow.commit()
