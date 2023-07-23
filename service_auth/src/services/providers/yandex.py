from fastapi import Depends
from functools import lru_cache
from sqlalchemy.ext.asyncio import AsyncSession
from yandexid import YandexID, YandexOAuth
from yandex_oauth import yao

from core.config import yandex_settings
from src.db.postgres import get_session, DbService
from src.schemas.entity import UserCreate
from src.models.entity import SocialAccount, User
from src.utils.base_utils import generate_random_string
from .base_login import OAuthLogin


class YandexProvider(OAuthLogin):
    def __init__(self, db_service=None) -> None:
        super(YandexProvider, self).__init__("yandex")
        self.yandex_oauth = YandexOAuth(
            client_id=yandex_settings.YANDEX_CLIENT_ID,
            client_secret=yandex_settings.YANDEX_CLIENT_SECRET,
            redirect_uri=yandex_settings.YANDEX_REDIRECT_URI,
        )
        self.db_service = db_service

    def get_auth_url(self):
        return self.yandex_oauth.get_authorization_url()

    async def register(self, code, auth_service):
        token = yao.get_token_by_code(
            code,
            yandex_settings.YANDEX_CLIENT_ID,
            yandex_settings.YANDEX_CLIENT_SECRET
        )
        social_user = YandexID(token.get('access_token'))
        user_data = social_user.get_user_info_json()

        account = await self.db_service.check_account_in_social(
            social_id=user_data.psuid,
            social_name='yandex'
        )
        if account:
            return account
        user = await self.db_service.simple_select(
            what_select=User,
            where_select=[User.email, user_data.default_email]
        )
        user_id = None
        email = None
        if len(user) == 1:
            user = user[0]
            user_id = user.id
            email = user.email
        elif len(user) == 0:
            user = await auth_service.create_user(
                UserCreate(
                    first_name=user_data.first_name,
                    last_name=user_data.last_name,
                    email=user_data.default_email,
                    password=generate_random_string())
            )
            user_id = user.id
            email = user.email
        else:
            return None

        # save data in social accounts
        social_account = SocialAccount(
            user=user, social_id=user_data.psuid, social_name="yandex"
        )
        await self.db_service.insert_data(data=social_account)
        return user_id, email


@lru_cache()
def yandex_provider(db: AsyncSession = Depends(get_session)) -> YandexProvider:
    return YandexProvider(
        db_service=DbService(db=db),
    )
