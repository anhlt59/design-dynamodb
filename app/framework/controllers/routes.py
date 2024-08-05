from flask import Flask

from .v1 import brand_view, category_view, order_view, product_view, user_view


def build_routes(app: Flask) -> None:
    # API V1
    prefix = "/api/v1"
    app.register_blueprint(brand_view, url_prefix=f"{prefix}/brands")
    app.register_blueprint(category_view, url_prefix=f"{prefix}/categories")
    app.register_blueprint(product_view, url_prefix=f"{prefix}/products")
    app.register_blueprint(user_view, url_prefix=f"{prefix}/users")
    app.register_blueprint(order_view, url_prefix=f"{prefix}/users/<user_id>")

    @app.route("/health")
    def health():
        return '{"status":true}', 200
