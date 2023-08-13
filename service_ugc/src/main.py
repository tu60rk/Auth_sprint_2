from fastapi import FastAPI
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from src.v1.producer.film_progress import router as film_progress_router
from src.core.config import ugc_settings
from fastapi.responses import ORJSONResponse


app = FastAPI(
    title=ugc_settings.PROJECT_NAME,
    description=ugc_settings.PROJECT_DESCRIPTION,
    version=ugc_settings.API_VERSION,
    docs_url='/api/v1/openapi',
    openapi_url='/api/v1/openapi.json',
    default_response_class=ORJSONResponse,
    root_path='/ugc',
    lifespan=lifespan,
)

app.include_router(film_progress_router, prefix='/api/v1/producer/film_progress')

loop = asyncio.get_event_loop()
aioproducer = AIOKafkaProducer(loop=loop, bootstrap_servers=ugc_settings.KAFKA_INSTANCE)

async def consume():
    consumer = AIOKafkaConsumer("test1", bootstrap_servers=ugc_settings.KAFKA_INSTANCE, loop=loop)
    await consumer.start()
    try:
        async for msg in consumer:
            print("consumed: ", msg.topic, msg.partition, msg.offset, msg.key, msg.value, msg.timestamp)
    finally:
        await consumer.stop()

@app.on_event("startup")
async def startup_event():
    await aioproducer.start()
    loop.create_task(consume())

@app.on_event("shutdown")
async def shutdown_event():
    await aioproducer.stop()

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        'main:app',
        host=ugc_settings.UGC_APP_HOST,
        port=ugc_settings.UGC_APP_PORT,
        reload=True,
    )
