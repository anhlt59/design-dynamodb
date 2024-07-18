from flask import Flask

from .controllers.brands import app as brand_app
from .controllers.categories import app as category_app
from .controllers.products import app as product_app
from .controllers.users import app as user_app


def build_routes(app: Flask) -> None:
    app.register_blueprint(brand_app, url_prefix="/api/v1/brands")
    app.register_blueprint(category_app, url_prefix="/api/v1/categories")
    app.register_blueprint(product_app, url_prefix="/api/v1/products")
    app.register_blueprint(user_app, url_prefix="/api/v1/users")

    @app.route("/health")
    def health():
        return '{"status":true}', 200
