import decimal
import traceback
from datetime import date, datetime

from flask import Flask, jsonify
from flask.json.provider import DefaultJSONProvider
from pynamodb.attributes import MapAttribute

from src.exceptions import ApiError
from src.models import DynamoModel


class ResponseErrorHandler:
    def __init__(self, app: Flask):
        @app.errorhandler(ApiError)
        def handle_api_error(error):
            app.logger.error(str(error))
            response = jsonify({"error": error.__class__.__name__, "message": str(error)})
            response.status_code = error.code
            return response

        @app.errorhandler(Exception)
        def handle_unknown_exception(error):
            app.logger.error(f"{str(error)} {traceback.format_exc().splitlines()}")
            response = jsonify({"error": "InternalServerError", "message": str(error)})
            response.status_code = 500
            return response


class ResponseJsonHandler(DefaultJSONProvider):
    @staticmethod
    def default(obj):
        """Serialize objects that aren't natively serializable by json.dumps."""
        if isinstance(obj, DynamoModel) or isinstance(obj, MapAttribute):
            return obj.to_dict()
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        if isinstance(obj, date) or isinstance(obj, datetime):
            return obj.isoformat()
        return DefaultJSONProvider.default(obj)


def configure_response_handlers(app):
    app.json_provider_class = ResponseJsonHandler
    app.json = ResponseJsonHandler(app)
    ResponseErrorHandler(app)
