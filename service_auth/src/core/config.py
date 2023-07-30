import os
from logging import config as logging_config
from pydantic import BaseSettings, Field

from src.core.logger import LOGGING


class Settings(BaseSettings):
	# Название проекта. Используется в Swagger-документации
	PROJECT_NAME: str = Field("Simple API for AUTH", env="PROJECT_NAME")
	PROJECT_DESCRIPTION: str = Field("Api's for authorisation and managing by roles.", env="PROJECT_DESCRIPTION")
	API_VERSION: str = Field("1.0.0", env="API_VERSION")

	# Настройка приложения
	AUTH_APP_HOST: str
	AUTH_APP_PORT: int
	AUTH_APP_NAME: str

	# Настройки Redis
	AUTH_REDIS_HOST: str
	AUTH_REDIS_PORT: int

	# Настройки Jaeger
	AUTH_JAEGER_HOST: str
	AUTH_JAEGER_PORT: int
	AUTH_JAEGER_ENABLE_TRACER: bool

	origins: list = [
		"http://localhost",
		"http://localhost:8000",
	]

	AUTH_POSTGRES_DB: str
	AUTH_POSTGRES_USER: str
	AUTH_POSTGRES_PASSWORD: str
	AUTH_POSTGRES_HOST: str
	AUTH_POSTGRES_PORT: int

	SAULT: str

	REQUEST_LIMIT_PER_MINUTE: int

	dsl_database: str = Field(
		None,
		env="AUTH_POSTGRES_DSL_DATABASE"
	)

	# Корень проекта
	base_dir: str = Field("", env="AUTH_BASE_DIR")

	class Config:
		case_sensitive = True
		env_file = "auth.env"


class JwtSettings(BaseSettings):
	JWT_PUBLIC_KEY: str
	JWT_PRIVATE_KEY: str
	REFRESH_TOKEN_EXPIRES_IN: int
	ACCESS_TOKEN_EXPIRES_IN: int
	JWT_ALGORITHM: str

	class Config:
		case_sensitive = True
		env_file = "jwt.env"


class YandexSettings(BaseSettings):
	YANDEX_CLIENT_ID: str
	YANDEX_CLIENT_SECRET: str
	YANDEX_REDIRECT_URI: str

	class Config:
		case_sensitive = True
		env_file = "providers.env"


settings = Settings()
yandex_settings = YandexSettings()
jwt_settings = JwtSettings()

settings.dsl_database = (
	f"postgresql+asyncpg://{settings.AUTH_POSTGRES_USER}:{settings.AUTH_POSTGRES_PASSWORD}@"
	f"{settings.AUTH_POSTGRES_HOST}:{settings.AUTH_POSTGRES_PORT}/{settings.AUTH_POSTGRES_DB}?async_fallback=True"
)

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)
