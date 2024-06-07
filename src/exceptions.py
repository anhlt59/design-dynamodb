from werkzeug import exceptions


class ApiError(Exception):
    pass


class ValidationError(ApiError, exceptions.BadRequest):
    code = 400


class BadRequestError(ApiError, exceptions.BadRequest):
    code = 400


class AuthenticationError(ApiError, exceptions.Unauthorized):
    code = 401


class AccessDeniedError(ApiError, exceptions.Forbidden):
    code = 403


class NotFoundError(ApiError, exceptions.NotFound):
    code = 404


class ConflictError(ApiError, exceptions.Conflict):
    code = 409


class UnprocessableEntityError(ApiError, exceptions.UnprocessableEntity):
    code = 422


class InternalServerError(ApiError, exceptions.InternalServerError):
    code = 500


# class NotImplementedError(ApiError, exceptions.NotImplemented):
#     code = 501


class ServiceUnavailableError(ApiError, exceptions.ServiceUnavailable):
    code = 503
