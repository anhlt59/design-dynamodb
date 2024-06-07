from flask import Flask
from flask_injector import FlaskInjector, request

from src import config
from src.middlewares import configure_response_handlers
from src.repositories import BrandRepository, CategoryRepository, OrderRepository, ProductRepository, UserRepository
from src.services import BrandService, CategoryService, OrderService, ProductService, UserService
from src.views.routes import build_routes


def create_app() -> Flask:
    app = Flask(config.NAME)
    app.config.from_object(config)
    app.secret_key = config.APP_SECRET_KEY

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
    user_service = UserService(user_repository)
    brand_service = BrandService(brand_repository, product_repository)
    category_service = CategoryService(category_repository)
    product_service = ProductService(product_repository)
    order_service = OrderService(order_repository, product_repository)
    # bind services to request scope
    binder.bind(UserService, to=user_service, scope=request)
    binder.bind(BrandService, to=brand_service, scope=request)
    binder.bind(CategoryService, to=category_service, scope=request)
    binder.bind(ProductService, to=product_service, scope=request)
    binder.bind(OrderService, to=order_service, scope=request)
