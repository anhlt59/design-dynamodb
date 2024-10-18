from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.adapters.api.containers import Container
from app.adapters.api.controllers import router
from app.common import configs
from app.common.exceptions import http as http_exceptions


def create_app() -> FastAPI:
    app = FastAPI(title=configs.NAME, openapi_url=configs.API_DOCS, debug=configs.DEBUG)
    app.container = Container()  # type: ignore
    build_api(app)
    add_middlewares(app)
    return app


def build_api(app: FastAPI):
    # build api routes
    app.include_router(router)

    # add exception handlers
    async def exception_handler(_: Request, exc: http_exceptions.HTTPException) -> JSONResponse:
        content = {"detail": exc.detail, "details": exc.details}
        return JSONResponse(status_code=exc.status_code, content=content)

    for exception in (
        http_exceptions.BadRequestException,
        http_exceptions.NotFoundException,
        http_exceptions.ForbiddenException,
        http_exceptions.UnauthorizedException,
        http_exceptions.UnprocessedException,
        http_exceptions.InternalServerError,
        http_exceptions.ConflictException,
    ):
        app.add_exception_handler(exception, handler=exception_handler)  # type: ignore


def add_middlewares(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,  # type: ignore
        allow_credentials=True,
        allow_origins=configs.CORS_ORIGINS,
        allow_methods=configs.CORS_METHODS,
        allow_headers=configs.COR_HEADERS,
    )
