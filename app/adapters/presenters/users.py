from .base import PageRequest, PageResponse, Response


class UserCreateRequest(Response):
    name: str
    email: str
    password: str


class UserUpdateRequest(Response):
    name: str | None = None
    password: str | None = None
    email: str | None = None


class UserResponse(Response):
    id: str
    name: str
    email: str
    createdAt: int
    updatedAt: int


class UsersRequest(PageRequest):
    name: str | None = None
    since: int | None = None
    until: int | None = None


class UsersResponse(PageResponse):
    items: list[UserResponse]
