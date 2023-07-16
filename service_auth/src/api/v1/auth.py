import logging

from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, Response, Request

from src.schemas.entity import (
    UserCreate, UserInDB, LoginUserSchema, Tokens, Status, RefreshToken
)
from src.services.auth import AuthService, auth_service
from src.utils.oauth2 import get_current_user


router = APIRouter()


@router.post(
    '/register',
    response_model=UserInDB,
    status_code=HTTPStatus.CREATED,
    summary="Регистрация пользователя",
    tags=["Авторизация"],
)
async def create_user(
    user_create: UserCreate,
    service_auth: AuthService = Depends(auth_service)
) -> UserInDB:
    result = await service_auth.create_user(
        user_info=user_create
    )

    if result == HTTPStatus.CONFLICT:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='User already registered'
        )
    if not result:
        raise HTTPException(
            status_code=HTTPStatus.BAD_GATEWAY,
            detail="Can't register user"
        )
    return result


@router.post(
    '/login',
    response_model=Tokens,
    status_code=HTTPStatus.ACCEPTED,
    summary="Аутентификация пользователя",
    tags=["Авторизация"],
)
async def login(
    payload: LoginUserSchema,
    request: Request,
    response: Response,
    service_auth: AuthService = Depends(auth_service)
):
    result = await service_auth.login(
        user_agent=request.headers.get('user-agent'),
        email=payload.email,
        passwd=payload.password,
        set_cookie=payload.set_cookie,
        response=response
    )

    if result == HTTPStatus.CONFLICT:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='User not found'
        )

    if result == HTTPStatus.UNAUTHORIZED:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Invalid password'
        )
    if not result:
        raise HTTPException(
            status_code=HTTPStatus.BAD_GATEWAY,
            detail="Can't login"
        )
    return result


@router.post(
    '/refresh',
    response_model=Tokens,
    status_code=HTTPStatus.ACCEPTED,
    summary="Перевыпустить токен",
    tags=["Авторизация"],
)
async def refresh(
    refresh_token: RefreshToken,
    request: Request,
    service_auth: AuthService = Depends(auth_service)
) -> Tokens:

    result = await service_auth.refresh(
        refresh_token=refresh_token.refresh_token,
        user_agent=request.headers.get('user-agent')
    )
    if not result:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Refresh token is invalid'
        )

    if result == HTTPStatus.CONFLICT:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='User not found'
        )

    if result == HTTPStatus.BAD_REQUEST:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Inactive user"
        )
    return result


@router.post(
    '/logout/all',
    response_model=Status,
    status_code=HTTPStatus.ACCEPTED,
    summary="Выйти из всех аккаунтов",
    tags=["Авторизация"],
)
async def logout_all(
    current_user: UserInDB = Depends(get_current_user),
    service_auth: AuthService = Depends(auth_service)
):
    user_id = str(current_user.id)
    result = await service_auth.logout_all(user_id=user_id)
    if not result:
        raise HTTPException(
            status_code=HTTPStatus.BAD_GATEWAY, detail="Can't logout"
        )
    return result


@router.post(
    '/logout/me',
    response_model=Status,
    status_code=HTTPStatus.ACCEPTED,
    summary="Выйти из текущего аккаунта",
    tags=["Авторизация"],
)
async def logout_me(
    request: Request,
    current_user: UserInDB = Depends(get_current_user),
    service_auth: AuthService = Depends(auth_service)
):
    user_agent = request.headers.get('user-agent')
    user_id = str(current_user.id)

    result = await service_auth.logout_me(
        user_agent=user_agent,
        user_id=user_id
    )
    if not result:
        raise HTTPException(
            status_code=HTTPStatus.BAD_GATEWAY, detail="Can't logout"
        )
    return result
