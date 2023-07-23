import os
import sys

sys.path.append(os.path.join(sys.path[0], 'src'))

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from redis.asyncio import Redis
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor


from api.v1 import auth, roles, users
from core.config import settings
from core.logger import LOGGING
from db import db_redis
from utils.jaeger import configure_tracer
from utils.limits import check_limit
import logging


@asynccontextmanager
async def lifespan(app: FastAPI):

    db_redis.redis = Redis(
        host=settings.AUTH_REDIS_HOST,
        port=settings.AUTH_REDIS_PORT
    )
    yield
    await db_redis.redis.close()


if settings.AUTH_JAEGER_ENABLE_TRACER:
    configure_tracer(settings.AUTH_JAEGER_HOST, settings.AUTH_JAEGER_PORT)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.API_VERSION,
    docs_url='/api/v1/openapi',
    openapi_url='/api/v1/openapi.json',
    default_response_class=ORJSONResponse,
    root_path='/auth',
    lifespan=lifespan,
)


@app.middleware('http')
async def before_request(request: Request, call_next):
    user_id = request.headers.get('X-Forwarded-For')
    request_id = request.headers.get('X-Request-Id')
    result = await check_limit(user_id=user_id)
    if result:
        return ORJSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={'detail': 'Too many requests'}
        )
    response = await call_next(request)
    if not request_id:
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'detail': 'X-Request-Id is required'}
        )
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


FastAPIInstrumentor.instrument_app(app)


app.include_router(auth.router, prefix='/api/v1/auth')
app.include_router(roles.router, prefix='/api/v1/roles')
app.include_router(users.router, prefix='/api/v1/users')


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.AUTH_APP_HOST,
        port=settings.AUTH_APP_PORT,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
