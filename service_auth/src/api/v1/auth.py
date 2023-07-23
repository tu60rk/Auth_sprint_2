from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, Response, Request
from fastapi.responses import RedirectResponse

from src.schemas.entity import (
    UserCreate, UserInDB, LoginUserSchema, Tokens, Status, RefreshToken, Login
)
from src.services.auth import AuthService, auth_service
from src.services.providers.yandex import yandex_provider, YandexProvider
from src.services.providers.base_login import OAuthLogin
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
    response_model=Login,
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

    if result == HTTPStatus.NOT_IMPLEMENTED:
        raise HTTPException(
            status_code=HTTPStatus.NOT_IMPLEMENTED,
            detail="Can't create tokens"
        )

    if not result:
        raise HTTPException(
            status_code=HTTPStatus.BAD_GATEWAY,
            detail="Can't login"
        )
    tokens, ex_user = result[0], result[1]
    return Login(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
        email=ex_user.email,
        user_id=ex_user.id,
        first_name=ex_user.first_name,
        last_name=ex_user.last_name
    )


@router.post(
    '/login/{provider}',
    response_class=RedirectResponse,
    status_code=HTTPStatus.SEE_OTHER,
    summary="Войти с помощью провайдера",
    tags=["Авторизация"],
)
async def provider_login(
    provider: str,
):
    provider = OAuthLogin.get_provider(provider)
    if provider:
        return provider.get_auth_url()
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail='Provider was not found'
    )


@router.get(
    '/login/yandex/redirect',
    response_model=Tokens,
    status_code=HTTPStatus.ACCEPTED,
    summary="Войти с помощью яндекса",
    tags=["Авторизация"],
)
async def yandex_login_redirect(
    code: int,
    request: Request,
    yandex_provider: YandexProvider = Depends(yandex_provider),
    auth_service: AuthService = Depends(auth_service)
):
    user_agent = request.headers.get("User-Agent")
    login_result = await auth_service.login_by_yandex(
        code=code, yandex_provider=yandex_provider, user_agent=user_agent
    )
    if login_result == HTTPStatus.CONFLICT:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='User not found'
        )

    if login_result == HTTPStatus.UNAUTHORIZED:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Invalid password'
        )
    if not login_result:
        raise HTTPException(
            status_code=HTTPStatus.BAD_GATEWAY,
            detail="Can't login"
        )
    return login_result


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

    if result == HTTPStatus.NOT_IMPLEMENTED:
        raise HTTPException(
            status_code=HTTPStatus.NOT_IMPLEMENTED,
            detail="Can't create tokens"
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
