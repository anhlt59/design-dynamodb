import os

DEBUG = os.getenv("DEBUG", True)
FLASK_ENV = os.getenv("FLASK_ENV", "test")
NAME = os.getenv("NAME", "app")

# App
APP_HOST = os.getenv("APP_HOST", "127.0.0.1")
APP_PORT = os.getenv("APP_PORT", "5000")
APP_URL = os.getenv("APP_URL", "http://localhost")

APP_API_KEY = os.getenv("APP_API_KEY", "012345678")
APP_SECRET_KEY = os.getenv("APP_SECRET_KEY", "012345678")

# AWS
AWS_ENDPOINT = os.getenv("AWS_ENDPOINT", "http://localhost:4566")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
DYNAMODB_DEFAULT_QUERY_LIMIT = os.getenv("DYNAMODB_DEFAULT_QUERY_LIMIT", 50)
DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME", "example")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
LOG_FORMAT = "%(asctime)s <%(module)s.%(funcName)s:%(lineno)s> - %(levelname)s - %(message)s"
