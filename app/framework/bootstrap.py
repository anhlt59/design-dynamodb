from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.common import constants, exceptions
from app.framework.containers import Container
from app.framework.controllers import router


def create_app() -> FastAPI:
    app = FastAPI(title=constants.NAME, openapi_url=constants.API_DOCS, debug=constants.DEBUG)
    app.container = Container()
    build_api(app)
    add_middlewares(app)
    return app


def build_api(app: FastAPI):
    # build api routes
    app.include_router(router)

    # add exception handlers
    async def exception_handler(_: Request, exc: exceptions.HTTPException) -> JSONResponse:
        content = {"detail": exc.detail, "details": exc.details}
        return JSONResponse(status_code=exc.status_code, content=content)

    for exception in (
        exceptions.BadRequestException,
        exceptions.NotFoundException,
        exceptions.ForbiddenException,
        exceptions.UnauthorizedException,
        exceptions.UnprocessableEntityException,
        exceptions.InternalServerError,
        exceptions.ConflictException,
    ):
        app.add_exception_handler(exception, handler=exception_handler)


def add_middlewares(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=constants.CORS_ORIGINS,
        allow_methods=constants.CORS_METHODS,
        allow_headers=constants.COR_HEADERS,
    )
