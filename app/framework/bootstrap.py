from flask import Flask
from flask_injector import FlaskInjector, request

from app.adapters.repositories import (
    BrandRepository,
    CategoryRepository,
    OrderRepository,
    ProductRepository,
    UserRepository,
)
from app.controllers import BrandController, CategoryController, OrderController, ProductController, UserController
from app.core import constants
from app.framework.middlewares import configure_response_handlers
from app.framework.views.routes import build_routes


def create_app() -> Flask:
    app = Flask(constants.NAME)
    app.config.from_object(constants)
    app.secret_key = constants.APP_SECRET_KEY

    build_routes(app)
    configure_response_handlers(app)
    FlaskInjector(app=app, modules=[_bind])
    return app


def _bind(binder):
    # init repositories
    user_repository = UserRepository()
    category_repository = CategoryRepository()
    brand_repository = BrandRepository()
    product_repository = ProductRepository()
    order_repository = OrderRepository()
    # init services
    user_controller = UserController(user_repository)
    brand_controller = BrandController(brand_repository, product_repository)
    category_controller = CategoryController(category_repository)
    product_controller = ProductController(product_repository)
    order_controller = OrderController(order_repository, product_repository)
    # bind services to request scope
    binder.bind(UserController, to=user_controller, scope=request)
    binder.bind(BrandController, to=brand_controller, scope=request)
    binder.bind(CategoryController, to=category_controller, scope=request)
    binder.bind(ProductController, to=product_controller, scope=request)
    binder.bind(OrderController, to=order_controller, scope=request)
