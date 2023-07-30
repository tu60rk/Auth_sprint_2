import os

from logging import config as logging_config
from pydantic import BaseSettings, Field

from core.logger import LOGGING


class Settings(BaseSettings):
    # Название проекта. Используется в Swagger-документации
    PROJECT_NAME: str = Field("Simple API for Cinema", env="PROJECT_NAME")
    PROJECT_DESCRIPTION: str = Field("Info about creators", env="PROJECT_DESCRIPTION")
    API_VERSION: str = Field("1.0.0", env="API_VERSION")

    FILM_APP_HOST: str
    FILM_APP_PORT: int

    FILM_REDIS_HOST: str
    FILM_REDIS_PORT: int

    FILM_ELASTIC_HOST: str
    FILM_ELASTIC_PORT: int

    REDIS_CACHE_EXPIRES: int = Field(60*5, env="REDIS_CACHE_EXPIRES")

    class Config:
        case_sensitive = True
        env_file = "film.env"
    # Настройка приложения
    # app_host = os.getenv("FILM_APP_HOST", "0.0.0.0")
    # app_port = int(os.getenv("FILM_APP_PORT", 8000))

    # # Настройки Redis
    # redis_host = os.getenv("FILM_REDIS_HOST", "127.0.0.1")
    # redis_port = int(os.getenv("FILM_REDIS_PORT", 6379))

    # # Настройки Elasticsearch
    # elastic_host = os.getenv("FILM_ELASTIC_HOST", "127.0.0.1")
    # elastic_port = int(os.getenv("FILM_ELASTIC_PORT", 9200))

    # # Корень проекта
    # base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # # Время хранения кэша в Redis
    # redis_cache_expires = 60 * 5


class JwtSettings(BaseSettings):
    JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str
    REFRESH_TOKEN_EXPIRES_IN: int
    ACCESS_TOKEN_EXPIRES_IN: int
    JWT_ALGORITHM: str

    class Config:
        case_sensitive = True
        env_file = "jwt.env"


settings = Settings()
jwt_settings = JwtSettings()


# Применяем настройки логирования
logging_config.dictConfig(LOGGING)
