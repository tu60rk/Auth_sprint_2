import json

from datetime import timedelta
from typing import Optional
from redis.asyncio import Redis
from src.core.config import settings

redis: Optional[Redis] = None


# Функция понадобится при внедрении зависимостей
async def get_redis() -> Optional[Redis]:
    redis = Redis(host=settings.redis_host, port=settings.redis_port)
    return redis


class RedisService:
    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    async def add_token(
        self,
        user_id: str,
        access_token: str,
        user_agent: str
    ) -> None:
        redis_user = await self.redis.get(user_id)
        values = json.loads(redis_user) if redis_user else {}
        values[user_agent] = access_token

        await self.redis.set(
            name=user_id,
            value=json.dumps(values),
            ex=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_IN)
        )

    async def get(self, user_id: str) -> Optional[dict]:
        return json.loads(await self.redis.get(str(user_id)))

    async def set(self, name: str, value: str, ex: timedelta = None):
        params = {
            "name": name,
            "value": value,
        }
        params.update({"ex": ex}) if ex else ''
        await self.redis.set(**params)

    async def delete(self, user_id: str):
        await self.redis.delete(user_id)
