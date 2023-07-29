import os
import sys


sys.path.append(os.path.join(sys.path[0], 'src'))

from contextlib import asynccontextmanager

import uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from api.v1 import films, persons, genres
from core.config import settings
from core.logger import LOGGING
from db import elastic
import logging


@asynccontextmanager
async def lifespan(app: FastAPI):

    es_url = f'http://{settings.FILM_ELASTIC_HOST}:{settings.FILM_ELASTIC_PORT}'
    redis_url = f'redis://{settings.FILM_REDIS_HOST}:{settings.FILM_REDIS_PORT}'

    # load services
    elastic.es = AsyncElasticsearch(hosts=[es_url])
    redis = aioredis.from_url(redis_url)
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')

    yield

    # close services and release the resources
    await elastic.elastic.close()
    await redis.close()


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.API_VERSION,
    docs_url='/api/v1/openapi',
    openapi_url='/api/v1/openapi.json',
    default_response_class=ORJSONResponse,
    root_path='/movies',
    lifespan=lifespan,
)

# Подключаем роутер к серверу, указав префикс /v1/films
# Теги указываем для удобства навигации по документации
app.include_router(films.router, prefix='/api/v1/films')
app.include_router(persons.router, prefix='/api/v1/persons')
app.include_router(genres.router, prefix='/api/v1/genres')


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.FILM_APP_HOST,
        port=settings.FILM_APP_PORT,
        reload=True,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
