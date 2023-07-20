import datetime
from redis.asyncio import Redis

from core.config import settings
from typing import Optional


redis_conn = Redis(host=settings.redis_host, port=settings.redis_port, db=3)


async def check_limit(user_id: str) -> Optional[bool]:
    pipe = redis_conn.pipeline()
    now = datetime.datetime.now()
    key = f'{user_id}:{now.minute}'
    await pipe.incr(key, 1)
    await pipe.expire(key, 59)
    result = await pipe.execute()
    request_number = result[0]
    if request_number > settings.REQUEST_LIMIT_PER_MINUTE:
        return True
