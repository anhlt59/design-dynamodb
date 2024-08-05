from flask import Flask

from .views import brand_view, category_view, order_view, product_view, user_view


def build_routes(app: Flask) -> None:
    app.register_blueprint(brand_view, url_prefix="/api/v1/brands")
    app.register_blueprint(category_view, url_prefix="/api/v1/categories")
    app.register_blueprint(product_view, url_prefix="/api/v1/products")
    app.register_blueprint(user_view, url_prefix="/api/v1/users")
    app.register_blueprint(order_view, url_prefix="/api/v1/users/<user_id>")

    @app.route("/health")
    def health():
        return '{"status":true}', 200
