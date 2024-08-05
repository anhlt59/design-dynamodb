import traceback
from functools import wraps

from flask import Flask, g, jsonify, request
from flask.json.provider import DefaultJSONProvider
from pynamodb.attributes import MapAttribute

from app.common.constants import APP_API_KEY
from app.common.exceptions import ApiError, AuthenticationError
from app.common.logger import logger


def api_key_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        api_key = request.headers.get("x-api-key")
        if api_key is None:
            raise AuthenticationError("Unauthorized - API key not found")
        if api_key != APP_API_KEY:
            raise AuthenticationError("Unauthorized - Invalid API key")
        g.request_timezone = request.headers.get("x-time-zone")
        return func(*args, **kwargs)

    return decorator


def configure_response_handlers(app):
    class ResponseErrorHandler:
        def __init__(self, _app: Flask):
            @_app.errorhandler(ApiError)
            def handle_api_error(error):
                logger.error(str(error))
                response = jsonify({"error": error.__class__.__name__, "message": str(error)})
                response.status_code = error.code
                return response

            @_app.errorhandler(Exception)
            def handle_unknown_exception(error):
                logger.error(f"{str(error)} {traceback.format_exc().splitlines()}")
                response = jsonify({"error": "InternalServerError", "message": str(error)})
                response.status_code = 500
                return response

    class ResponseJsonHandler(DefaultJSONProvider):
        @staticmethod
        def default(obj):
            """Serialize objects that aren't natively serializable by json.dumps."""
            if isinstance(obj, MapAttribute):
                return obj.to_dict()
            return DefaultJSONProvider.default(obj)

    app.json_provider_class = ResponseJsonHandler
    app.json = ResponseJsonHandler(app)
    ResponseErrorHandler(app)
