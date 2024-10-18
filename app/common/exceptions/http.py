from typing import Any


class HTTPException(Exception):
    status_code = 500

    def __init__(self, detail: str | None = None, details: list[Any] | None = None):
        self.detail = detail
        self.details = details
        super().__init__(detail)


class BadRequestException(HTTPException):
    status_code = 400


class NotFoundException(HTTPException):
    status_code = 404


class ForbiddenException(HTTPException):
    status_code = 403


class UnauthorizedException(HTTPException):
    status_code = 401


class UnprocessedException(HTTPException):
    status_code = 422


class ConflictException(HTTPException):
    status_code = 409


class InternalServerError(HTTPException):
    status_code = 500
