import datetime
from redis.asyncio import Redis

from core.config import settings, jwt_settings
from typing import Optional


redis_conn = Redis(host=settings.AUTH_REDIS_HOST, port=settings.AUTH_REDIS_PORT, db=3)


async def check_limit(user_id: str) -> Optional[bool]:
    pipe = redis_conn.pipeline()
    now = datetime.datetime.now()
    key = f'{user_id}:{now.minute}'
    await pipe.incr(key, 1)
    await pipe.expire(key, 59)
    result = await pipe.execute()
    request_number = result[0]
    if request_number > jwt_settings.REQUEST_LIMIT_PER_MINUTE:
        return True
