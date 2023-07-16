import json

from fastapi import Depends, HTTPException, status, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from src.db.postgres import get_session
from src.db.db_redis import get_redis
from src.core.oauth2 import AuthJWT
from src.schemas.entity import UserInDB
from src.models.entity import User


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(HTTPBearer()),
    redis: Redis = Depends(get_redis),
    db: AsyncSession = Depends(get_session),
    Authorize: AuthJWT = Depends(),
) -> UserInDB:

    token = credentials.credentials

    # проверка токена
    try:
        await Authorize._verifying_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token is expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    data_token = await Authorize.get_raw_jwt(token)
    if token and data_token['type'] != 'access':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # нужно проверить в redis наличие токена по юзеру
    user_tokens = json.loads(await redis.get(data_token.get('sub')))
    if token not in user_tokens.values():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # проверить usera в бд
    existing_user = await db.execute(
        select(User).where(User.email == data_token.get('email'))
    )
    existing_user = existing_user.scalar()
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not existing_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return UserInDB(
        id=data_token.get('sub'),
        email=data_token.get('email'),
        role_id=data_token.get('role_id')
    )
