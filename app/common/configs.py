import os

# App
NAME = os.getenv("NAME", "app")
HOST = os.getenv("APP_HOST", "127.0.0.1")
PORT = int(os.getenv("APP_PORT", 5000))
API_DOCS = os.getenv("API_DOCS", "/api/openapi.json")
API_KEY = os.getenv("API_KEY", "0123456789")
SECRET_KEY = os.getenv("APP_SECRET_KEY", "012345678")
DEBUG = os.getenv("DEBUG", "true") == "true"

# CORS settings
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
CORS_METHODS = os.getenv("CORS_METHODS", "*").split(",")
COR_HEADERS = os.getenv("CORS_HEADERS", "*").split(",")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
LOG_FORMAT = "%(asctime)s <%(module)s.%(funcName)s:%(lineno)s> - %(levelname)s - %(message)s"

# AWS
DYNAMODB_ENDPOINT = os.getenv("AWS_ENDPOINT", "http://localhost:4566")
DYNAMODB_REGION = os.getenv("AWS_REGION", "us-east-1")
DYNAMODB_DEFAULT_QUERY_LIMIT = os.getenv("DYNAMODB_DEFAULT_QUERY_LIMIT", 50)
DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME", "example")
