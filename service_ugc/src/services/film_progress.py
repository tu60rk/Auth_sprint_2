import asyncio
import json
import logging

from aiokafka import AIOKafkaProducer

from src.models.film_progress import FilmProgress
from src.core.config import ugc_settings

loop = asyncio.get_event_loop()
logger = logging.getLogger(__name__)


async def producer(topic: str, key: str, msg: str):
    producer = AIOKafkaProducer(
        bootstrap_servers=ugc_settings.KAFKA_INSTANCE)
    await producer.start()
    try:
        await producer.send_and_wait(topic=topic, key=key, value=msg)
    finally:
        await producer.stop()


async def record_progress(msg: FilmProgress, topic: str) -> bool:
    try:
        dict_data = msg.dict()
        dict_data['movie_id'] = str(dict_data['movie_id'])
        dict_data['user_id'] = str(dict_data['user_id'])
        dict_data['event_date'] = dict_data['event_date'].strftime('%d.%m.%Y %H%:%M:%S')
        data = json.dumps(dict_data).encode("ascii")
        key = f'{msg.movie_id}:{msg.user_id}'.encode('ascii')

        await producer(topic=topic, key=key, msg=data)
    except Exception as err:
        logger.debug(err)
        return False
    return True
