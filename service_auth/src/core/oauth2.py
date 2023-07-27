import base64
from typing import List
from async_fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel

from .config import jwt_settings


class Settings(BaseModel):
    authjwt_algorithm: str = jwt_settings.JWT_ALGORITHM
    authjwt_decode_algorithms: List[str] = [jwt_settings.JWT_ALGORITHM]
    authjwt_token_location: set = {'cookies', 'headers'}
    authjwt_access_cookie_key: str = 'access_token'
    authjwt_refresh_cookie_key: str = 'refresh_token'
    authjwt_cookie_csrf_protect: bool = True
    authjwt_public_key: str = base64.b64decode(
        jwt_settings.JWT_PUBLIC_KEY).decode('utf-8')
    authjwt_private_key: str = base64.b64decode(
        jwt_settings.JWT_PRIVATE_KEY).decode('utf-8')


@AuthJWT.load_config
def get_config():
    return Settings()
