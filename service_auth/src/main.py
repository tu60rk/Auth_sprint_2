import os
import sys
import logging
import time
import random
import string
from uuid import uuid4
from contextvars import ContextVar


sys.path.append(os.path.join(sys.path[0], 'src'))

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from redis.asyncio import Redis
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider        
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter


from api.v1 import auth, roles, users
from core.config import settings
from core.logger import LOGGING
from db import db_redis
import logging



origins = [
    "http://localhost",
    "http://localhost:8000",
]

REQUEST_ID_CTX_KEY = 'request_id'
_request_id_ctx_var: ContextVar[str] = ContextVar(REQUEST_ID_CTX_KEY, default=None)


def configure_tracer() -> None:
    trace.set_tracer_provider(TracerProvider())
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name='localhost',
                agent_port=6831,
            )
        )
    )
    # Чтобы видеть трейсы в консоли
    # trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))


def get_request_id() -> str:
    return _request_id_ctx_var.get()


@asynccontextmanager
async def lifespan(app: FastAPI):

    db_redis.redis = Redis(
        host=settings.redis_host,
        port=settings.redis_port
    )
    yield
    await db_redis.redis.close()


configure_tracer()
app = FastAPI(
    title=settings.project_name,
    description=settings.project_description,
    version=settings.api_version,
    docs_url='/api/v1/openapi',
    openapi_url='/api/v1/openapi.json',
    default_response_class=ORJSONResponse,
    root_path='/auth',
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.middleware('http')
async def before_request(request: Request, call_next):
    request_id = _request_id_ctx_var.set(str(uuid4()))
    response = await call_next(request)
    response.headers['X-Request-Id'] = get_request_id()

    _request_id_ctx_var.reset(request_id)

    if not request_id:
        return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'detail': 'X-Request-Id is required'})
    return response


FastAPIInstrumentor.instrument_app(app)


app.include_router(auth.router, prefix='/api/v1/auth')
app.include_router(roles.router, prefix='/api/v1/roles')
app.include_router(users.router, prefix='/api/v1/users')

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.app_host,
        port=settings.app_port,
        reload=True,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
