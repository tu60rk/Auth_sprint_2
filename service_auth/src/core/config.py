import os
from logging import config as logging_config
from pydantic import BaseSettings, Field

from src.core.logger import LOGGING


class Settings(BaseSettings):
    # Название проекта. Используется в Swagger-документации
    project_name: str = Field("Simple API for AUTH", env="PROJECT_NAME")
    project_description: str = Field("Api's for authorisation and managing by roles.", env="PROJECT_DESCRIPTION")
    api_version: str = Field("1.0.0", env="API_VERSION")

    # Настройка приложения
    app_host: str = Field("0.0.0.0", env="AUTH_APP_HOST")
    app_port: int = Field(8001, env="AUTH_APP_PORT")
    app_name: str = Field("auth_service", env="AUTH_APP_NAME")

    # Настройки Redis
    redis_host: str = Field("127.0.0.1", env="AUTH_REDIS_HOST")
    redis_port: int = Field(6378, env="AUTH_REDIS_PORT")

    # Настройки Jaeger
    jaeger_host: str = Field("auth_jaeger", env="AUTH_JAEGER_HOST")
    jaeger_port: int = Field(6831, env="AUTH_JAEGER_PORT")
    enable_tracer: bool = os.getenv("AUTH_JAEGER_ENABLE_TRACER", False).lower() == "True"

    origins: list = [
        "http://localhost",
        "http://localhost:8000",
    ]

    db_name: str = Field("auth_database", env="AUTH_POSTGRES_DB")
    db_user: str = Field("auth", env="AUTH_POSTGRES_USER")
    db_password: str = Field(None, env="AUTH_POSTGRES_PASSWORD")
    db_host: str = Field("auth_db", env="AUTH_POSTGRES_HOST")
    db_port: int = Field(5432, env="AUTH_POSTGRES_PORT")

    dsl_database: str = Field(
        None,
        env="AUTH_POSTGRES_DSL_DATABASE"
    )

    # Корень проекта
    base_dir: str = Field("", env="AUTH_BASE_DIR")

    JWT_PUBLIC_KEY: str = Field(None, env="JWT_PUBLIC_KEY")
    JWT_PRIVATE_KEY: str = Field(None, env="JWT_PRIVATE_KEY")
    REFRESH_TOKEN_EXPIRES_IN: int = Field(15, env="REFRESH_TOKEN_EXPIRES_IN")
    ACCESS_TOKEN_EXPIRES_IN: int = Field(60, env="ACCESS_TOKEN_EXPIRES_IN")
    JWT_ALGORITHM: str = Field("RS256", env="ALGORITHM")
    SAULT: str = Field("", env="SAULT")

    REQUEST_LIMIT_PER_MINUTE: int = Field(20, env="REQUEST_LIMIT_PER_MINUTE")

settings = Settings()

settings.dsl_database = (
    f"postgresql+asyncpg://{settings.db_user}:{settings.db_password}@"
    f"{settings.db_host}:{settings.db_port}/{settings.db_name}?async_fallback=True"
)

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)
