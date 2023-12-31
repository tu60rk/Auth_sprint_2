import json
import uuid

from functools import lru_cache
from typing import Optional
from http import HTTPStatus
from fastapi import Depends, Response
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import true, false
from redis.asyncio import Redis
from werkzeug.security import check_password_hash
from datetime import timedelta

from src.db.postgres import get_session, DbService
from src.db.db_redis import get_redis, RedisService
from src.schemas.entity import Status, UserInDB, Tokens
from src.models.entity import (
    Role, User, UserRoles, RefreshToken, AccountHistory
)
from src.core.config import jwt_settings
from core.oauth2 import AuthJWT
from .providers.yandex import YandexProvider


class AuthService:
    def __init__(
        self,
        db_service: DbService,
        redis_service: RedisService,
        authorize: AuthJWT
    ) -> None:
        self.redis_service = redis_service
        self.authorize = authorize
        self.db_service = db_service

    async def __create_tokens(
        self,
        subject: str,
        user_claims: dict,
        is_ex: bool = True,
    ) -> Tokens:

        params_for_access = {
            'subject': subject,
            'user_claims': user_claims
        }

        params_for_refresh = {
            'subject': subject,
        }

        if is_ex:
            params_for_access.update(
                {
                    "expires_time": timedelta(
                        minutes=jwt_settings.ACCESS_TOKEN_EXPIRES_IN
                    )
                }
            )

            params_for_refresh.update(
                {
                    "expires_time": timedelta(
                        days=jwt_settings.REFRESH_TOKEN_EXPIRES_IN
                    )
                }
            )

        access_token = await self.authorize.create_access_token(
            **params_for_access
        )
        refresh_token = await self.authorize.create_refresh_token(
            **params_for_access
        )
        return Tokens(access_token=access_token, refresh_token=refresh_token)

    async def __create_roles(self) -> None:
        user_role = Role(
            name='user',
            description='user'
        )
        admin_role = Role(
            name='admin',
            description='admin'
        )

        await self.db_service.insert_data(user_role)
        await self.db_service.insert_data(admin_role)

    async def __check_user_exist_active(
        self,
        by: str,
        data: str
    ) -> Optional[HTTPStatus]:
        where_list = []
        if by == 'email':
            where_list = [User.email, data]
        else:
            where_list = [User.id, data]
        existing_user = await self.db_service.simple_select(
            what_select=User,
            where_select=where_list
        )
        if len(existing_user) == 0:
            return HTTPStatus.CONFLICT
        if not existing_user[0].is_active:
            return HTTPStatus.BAD_REQUEST
        return existing_user[0]

    async def __generate_and_save_tokens(
        self,
        user_id: uuid.UUID,
        email: str,
        user_agent: str,
    ) -> Tokens:
        try:
            user_roles = await self.db_service.get_user_roles(
                    user_id=user_id
                )

            # create access and refresh tokens
            tokens = await self.__create_tokens(
                subject=str(user_id),
                is_ex=True,
                user_claims={
                    "roles": user_roles,
                    "email": email
                }
            )
            # save access token
            await self.redis_service.add_token(
                user_id=str(user_id),
                access_token=tokens.access_token,
                user_agent=user_agent
            )
            # save refresh token
            data_refresh_token = RefreshToken(
                user_id=user_id,
                user_token=tokens.refresh_token,
                is_active=true(),
                user_agent=user_agent
            )
            await self.db_service.insert_data(data_refresh_token)
            return tokens
        except Exception:
            return None

    async def create_user(self, user_info: UserInDB) -> Optional[UserInDB]:
        try:
            user_dto = jsonable_encoder(user_info)
            user_dto['password'] = jwt_settings.SAULT + user_dto['email'] + user_dto['password']
            user = User(**user_dto)

            roles = await self.db_service.simple_select(
                what_select=Role.id,
                where_select=[Role.name, 'user']
            )

            if len(roles) == 0:
                await self.__create_roles()
                roles = await self.db_service.simple_select(
                    what_select=Role.id,
                    where_select=[Role.name, 'user']
                )

            existing_user = await self.db_service.simple_select(
                what_select=User,
                where_select=[User.email, user.email]
            )
            if len(existing_user) > 0:
                return HTTPStatus.CONFLICT

            user.verified = True
            await self.db_service.insert_data(data=user)
            await self.db_service.simple_insert(
                what_insert=UserRoles,
                values_insert={
                    'user_id': user.id,
                    'role_id': roles[0]
                }
            )
            return user
        except Exception:
            return None

    async def login(
        self,
        user_agent: str,
        email: str,
        passwd: str,
        set_cookie: bool,
        response: Response
    ):

        try:
            existing_user = await self.__check_user_exist_active(
                by='email',
                data=email
            )
            if existing_user in [HTTPStatus.CONFLICT, HTTPStatus.BAD_REQUEST]:
                return existing_user

            password_match = check_password_hash(
                pwhash=existing_user.hash_password,
                password=jwt_settings.SAULT + existing_user.email + passwd
            )

            if not password_match:
                return HTTPStatus.UNAUTHORIZED

            tokens = await self.__generate_and_save_tokens(
                user_id=existing_user.id,
                email=existing_user.email,
                user_agent=user_agent,
            )
            if tokens is None:
                return HTTPStatus.NOT_IMPLEMENTED
            # add data to account history
            data_header = AccountHistory(
                user_id=existing_user.id,
                user_agent=user_agent
            )
            await self.db_service.insert_data(data_header)
            # set cookie
            if set_cookie:
                response.set_cookie('access_token', tokens.access_token, jwt_settings.ACCESS_TOKEN_EXPIRES_IN, jwt_settings.ACCESS_TOKEN_EXPIRES_IN, '/', None, False, True, 'lax')
                response.set_cookie('refresh_token', tokens.refresh_token, jwt_settings.REFRESH_TOKEN_EXPIRES_IN, jwt_settings.REFRESH_TOKEN_EXPIRES_IN, '/', None, False, True, 'lax')
        except Exception:
            return None
        return tokens, existing_user

    async def login_by_yandex(
        self,
        code: int,
        yandex_provider: YandexProvider,
        user_agent: str
    ) -> Tokens:
        result = await yandex_provider.register(code, self)
        if result is None:
            return HTTPStatus.BAD_REQUEST

        user_id, email = result[0], result[1]
        tokens = await self.__generate_and_save_tokens(
                user_id=user_id,
                email=email,
                user_agent=user_agent
            )
        if tokens is None:
            return HTTPStatus.CONFLICT
        return tokens

    async def refresh(self, refresh_token: str, user_agent: str) -> Tokens:
        # check token
        try:
            await self.authorize._verify_jwt_in_request(
                token=refresh_token,
                type_token='refresh',
                token_from='headers'
            )

            # check user
            data_token = await self.authorize.get_raw_jwt(refresh_token)
            sub = data_token.get('sub')
            existing_user = await self.__check_user_exist_active(
                by='user',
                data=sub
            )
            if existing_user in [HTTPStatus.CONFLICT, HTTPStatus.BAD_REQUEST]:
                return existing_user

            # change status for refresh token
            await self.db_service.simple_update(
                what_update=RefreshToken,
                where_update=[RefreshToken.user_token, refresh_token],
                values_update={'is_active': false()}
            )
            tokens = await self.__generate_and_save_tokens(
                user_id=existing_user.id,
                email=existing_user.email,
                user_agent=user_agent
            )
            if tokens is None:
                return HTTPStatus.NOT_IMPLEMENTED
        except Exception:
            return None
        return tokens

    async def logout_all(self, user_id: str) -> Status:
        try:
            await self.redis_service.delete(user_id)
            await self.db_service.simple_update(
                what_update=RefreshToken,
                where_update=[RefreshToken.user_id, user_id],
                values_update={'is_active': false()}
            )
        except Exception:
            return None
        return Status(status='success')

    async def logout_me(self, user_id: str, user_agent: str) -> Status:

        try:
            current_user_tokens = await self.redis_service.get(user_id)
            current_user_tokens.pop(user_agent)

            if len(current_user_tokens) == 0:
                await self.redis_service.delete(user_id)
            else:
                await self.redis_service.set(
                    name=user_id,
                    value=json.dumps(current_user_tokens),
                )

            await self.db_service.update_token(
                what_update=RefreshToken,
                where_update={
                    'user_id': user_id,
                    'user_agent': user_agent,
                    'is_active': true()
                },
                values_update={'is_active': false()}
            )

        except Exception:
            return None

        return Status(status='success')


@lru_cache()
def auth_service(
    db: AsyncSession = Depends(get_session),
    redis: Redis = Depends(get_redis),
    authorize: AuthJWT = Depends()
) -> AuthService:
    return AuthService(
        db_service=DbService(db=db),
        redis_service=RedisService(redis=redis),
        authorize=authorize,
    )
