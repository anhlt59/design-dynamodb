from functools import wraps

from flask import g, request

from src.config import APP_API_KEY
from src.exceptions import AuthenticationError


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
