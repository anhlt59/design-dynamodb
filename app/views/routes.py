from flask import Flask

from .controllers import brand_controller, category_controller, order_controller, product_controller, user_controller


def build_routes(app: Flask) -> None:
    app.register_blueprint(brand_controller, url_prefix="/api/v1/brands")
    app.register_blueprint(category_controller, url_prefix="/api/v1/categories")
    app.register_blueprint(product_controller, url_prefix="/api/v1/products")
    app.register_blueprint(user_controller, url_prefix="/api/v1/users")
    app.register_blueprint(order_controller, url_prefix="/api/v1/users/<user_id>")

    @app.route("/health")
    def health():
        return '{"status":true}', 200
