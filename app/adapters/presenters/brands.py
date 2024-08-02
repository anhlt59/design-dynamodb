from .base import PageRequest, PageResponse, Response


class BrandCreateRequest(Response):
    name: str


class BrandUpdateRequest(Response):
    name: str


class BrandResponse(Response):
    id: str
    name: str
    createdAt: int
    updatedAt: int


class BrandsRequest(PageRequest):
    name: str | None = None

    @property
    def filters(self):
        return {"name": self.name}


class BrandsResponse(PageResponse):
    items: list[BrandResponse]
