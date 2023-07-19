import jwt
import time
import http
import base64
import aiohttp

from typing import Optional
from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.core.config import settings


class JWTBearer(HTTPBearer):
    def __init__(self, check_user: bool = False, auto_error: bool = True):
        super().__init__(auto_error=auto_error)
        self.check_user = check_user

    async def __call__(self, request: Request) -> dict:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if not credentials:
            raise HTTPException(
                status_code=http.HTTPStatus.FORBIDDEN,
                detail='Invalid authorization code'
            )
        if not credentials.scheme == 'Bearer':
            raise HTTPException(
                status_code=http.HTTPStatus.UNAUTHORIZED,
                detail='Only Bearer token might be accepted'
            )
        decoded_token = self.parse_token(credentials.credentials)
        if not decoded_token:
            raise HTTPException(
                    status_code=http.HTTPStatus.FORBIDDEN,
                    detail='Invalid or expired token'
                )

        if self.check_user:
            # проверить usera в бд
            response = await self.check(
                'http://auth_service:8000/api/v1/users/me',
                params={},
                headers={'Authorization': f'Bearer {credentials.credentials}'}
            )
            if response.status != http.HTTPStatus.ACCEPTED:
                raise HTTPException(
                    status_code=http.HTTPStatus.FORBIDDEN,
                    detail="User doesn't exist"
                )
        return decoded_token

    @staticmethod
    def parse_token(jwt_token: str) -> Optional[dict]:
        try:
            decoded_token = jwt.decode(
                jwt_token,
                key=base64.b64decode(settings.JWT_PUBLIC_KEY).decode('utf-8'),
                algorithms=[settings.JWT_ALGORITHM]
            )
            return decoded_token if decoded_token['exp'] >= time.time() else None
        except Exception:
            return None

    @staticmethod
    async def check(query: str, params: dict = {}, headers: dict= {}, json: dict = {}):
        async with aiohttp.ClientSession(headers=headers) as client:
            response = await client.get(query, json=json, params=params)
        return response


security_jwt = JWTBearer()
security_jwt_check = JWTBearer(check_user=True)
