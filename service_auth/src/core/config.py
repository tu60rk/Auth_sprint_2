import os
from logging import config as logging_config
from pydantic import BaseSettings

from src.core.logger import LOGGING


class Settings(BaseSettings):
    # Название проекта. Используется в Swagger-документации
    project_name: str = os.getenv("PROJECT_NAME", "Simple API for AUTH")
    project_description: str = os.getenv("PROJECT_DESCRIPTION", "Api's for authorisation and managing by roles.")
    api_version: str = os.getenv("API_VERSION", "1.0.0")

    # Настройка приложения
    app_host: str = os.getenv("AUTH_APP_HOST", "0.0.0.0")
    app_port: int = int(os.getenv("AUTH_APP_PORT", 8001))
    app_name: str = os.getenv("AUTH_APP_NAME", "auth_service")

    # Настройки Redis
    redis_host: str = os.getenv("AUTH_REDIS_HOST", "127.0.0.1")
    redis_port: int = int(os.getenv("AUTH_REDIS_PORT", 6378))

    # Настройки Jaeger
    jaeger_host: str = os.getenv("AUTH_JAEGER_HOST", "auth_jaeger")
    jaeger_port: int = int(os.getenv("AUTH_JAEGER_PORT", 6831))
    enable_tracer: bool = os.getenv("AUTH_JAEGER_ENABLE_TRACER", False) == "True"

    db_name: str = os.getenv("AUTH_POSTGRES_DB", "auth_database")
    db_user: str = os.getenv("AUTH_POSTGRES_USER", "auth")
    db_password: str = os.getenv("AUTH_POSTGRES_PASSWORD", None)
    db_host: str = os.getenv("AUTH_POSTGRES_HOST", "postgres")
    db_port: int = int(os.getenv("AUTH_POSTGRES_PORT", 5432))
    dsl_database: str = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?async_fallback=True"
    # Корень проекта
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    JWT_PUBLIC_KEY: str = os.getenv('JWT_PUBLIC_KEY', None)
    JWT_PRIVATE_KEY: str = os.getenv('JWT_PRIVATE_KEY', None)
    REFRESH_TOKEN_EXPIRES_IN: int = os.getenv('REFRESH_TOKEN_EXPIRES_IN', 15)
    ACCESS_TOKEN_EXPIRES_IN: int = os.getenv('ACCESS_TOKEN_EXPIRES_IN', 60)
    JWT_ALGORITHM: str = os.getenv('ALGORITHM', 'RS256')
    SAULT: str = os.getenv('SAULT', '')

    REQUEST_LIMIT_PER_MINUTE: int = os.getenv('REQUEST_LIMIT_PER_MINUTE', 20)


settings = Settings()

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)
