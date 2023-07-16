import os

from pydantic import BaseSettings


class TestSettings(BaseSettings):
    # Название проекта. Используется в Swagger-документации
    project_name: str = os.getenv("PROJECT_NAME", "Simple API for Cinema")
    project_description: str = os.getenv("PROJECT_DESCRIPTION", "Info about creators")
    api_version: str = os.getenv("API_VERSION", "1.0.0")

    # Настройка приложения
    app_host: str = os.getenv("APP_HOST", "127.0.0.1")
    app_port: int = int(os.getenv("APP_PORT", 8000))
    app_api_host: str = f'http://auth_service:{app_port}/api/v1/'

    # Настройки Redis
    redis_host: str = os.getenv("REDIS_HOST", "127.0.0.1")
    redis_port: int = int(os.getenv("REDIS_PORT", 6379))
    redis_db_test: int = int(os.getenv("REDIS_DB_TEST", 6))
    
    # Настройки DB postgres
    db_name: str = os.getenv("POSTGRES_DB", "auth_database")
    db_user: str = os.getenv("POSTGRES_USER", "auth")
    db_password: str = os.getenv("POSTGRES_PASSWORD", None)
    db_host: str = os.getenv("POSTGRES_HOST", "postgres")
    db_port: int = int(os.getenv("POSTGRES_PORT", 5432))
    dsl_database: str = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?async_fallback=True"

    # Корень проекта
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


test_settings = TestSettings()
