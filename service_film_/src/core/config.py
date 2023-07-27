import os

from logging import config as logging_config
from pydantic import BaseSettings

from core.logger import LOGGING


class Settings(BaseSettings):
    # Название проекта. Используется в Swagger-документации
    project_name = os.getenv("PROJECT_NAME", "Simple API for Cinema")
    project_description = os.getenv("PROJECT_DESCRIPTION", "Info about creators")
    api_version = os.getenv("API_VERSION", "1.0.0")

    # Настройка приложения
    app_host = os.getenv("FILM_APP_HOST", "0.0.0.0")
    app_port = int(os.getenv("FILM_APP_PORT", 8000))

    # Настройки Redis
    redis_host = os.getenv("FILM_REDIS_HOST", "127.0.0.1")
    redis_port = int(os.getenv("FILM_REDIS_PORT", 6379))

    # Настройки Elasticsearch
    elastic_host = os.getenv("FILM_ELASTIC_HOST", "127.0.0.1")
    elastic_port = int(os.getenv("FILM_ELASTIC_PORT", 9200))

    # Корень проекта
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Время хранения кэша в Redis
    redis_cache_expires = 60 * 5

class JwtSettings(BaseSettings):
	JWT_PUBLIC_KEY: str
	JWT_PRIVATE_KEY: str
	REFRESH_TOKEN_EXPIRES_IN: int
	ACCESS_TOKEN_EXPIRES_IN: int
	JWT_ALGORITHM: str
	SAULT: str

	REQUEST_LIMIT_PER_MINUTE: int

	class Config:
		case_sensitive = True
		env_file = "jwt.env"

settings = Settings()
jwt_settings = JwtSettings()


# Применяем настройки логирования
logging_config.dictConfig(LOGGING)
