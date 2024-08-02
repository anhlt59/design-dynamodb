from .base import PageRequest, PageResponse, Response


class CategoryCreateRequest(Response):
    name: str


class CategoryUpdateRequest(Response):
    name: str


class CategoryResponse(Response):
    id: str
    name: str
    createdAt: int
    updatedAt: int


class CategoriesRequest(PageRequest):
    name: str | None = None

    @property
    def filters(self):
        return {"name": self.name}


class CategoriesResponse(PageResponse):
    items: list[CategoryResponse]
