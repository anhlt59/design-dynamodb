from .base import PageRequest, PageResponse, Response


class ProductCreateRequest(Response):
    name: str
    price: float
    stock: int
    categoryId: str
    brandId: str


class ProductUpdateRequest(Response):
    name: str | None = None
    price: float | None = None
    stock: int | None = None
    categoryId: str | None = None
    brandId: str | None = None


class ProductResponse(Response):
    id: str
    name: str
    price: float
    stock: int
    categoryId: str
    brandId: str
    createdAt: int
    updatedAt: int


class ProductsRequest(PageRequest):
    name: str | None = None
    categoryId: str | None = None
    brandId: str | None = None
    priceGT: float | None = None
    priceLT: float | None = None
    since: int | None = None
    until: int | None = None

    @property
    def filters(self):
        return {
            "name": self.name,
            "categoryId": self.categoryId,
            "brandId": self.brandId,
            "priceGT": self.priceGT,
            "priceLT": self.priceLT,
            "since": self.since,
            "until": self.until,
        }


class ProductsResponse(PageResponse):
    items: list[ProductResponse]
