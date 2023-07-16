from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List

from src.utils.oauth2 import get_current_user
from src.schemas.entity import (
    ShemaAccountHistory, Status, UserInDB, ChangePassword, ChangeEmail
)
from src.services.users import user_service, UserService

router = APIRouter()


@router.get(
    "/me",
    response_model=UserInDB,
    status_code=HTTPStatus.ACCEPTED,
    summary="Кто я",
    tags=['Пользователь']
)
async def read_users_me(current_user: UserInDB = Depends(get_current_user)):
    return current_user


@router.get(
    "/account-history",
    response_model=List[ShemaAccountHistory],
    status_code=HTTPStatus.ACCEPTED,
    summary="История входов",
    tags=['Пользователь']
)
async def get_account_history(
    current_user: UserInDB = Depends(get_current_user),
    service_user: UserService = Depends(user_service),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
) -> List[ShemaAccountHistory]:
    result = await service_user.get_account_history(current_user.id)
    if not result:
        raise HTTPException(
            status_code=HTTPStatus.BAD_GATEWAY,
            detail="Can't get account history"
        )

    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    paginated_result = result[start_index:end_index]

    return paginated_result


@router.put(
    "/password",
    response_model=Status,
    status_code=HTTPStatus.ACCEPTED,
    summary="Смена пароля",
    tags=['Пользователь']
)
async def change_password(
    change_password_data: ChangePassword,
    current_user: UserInDB = Depends(get_current_user),
    service_user: UserService = Depends(user_service),
 ):

    if change_password_data.password != change_password_data.repeat_password:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='New password and repeat password do not match'
        )

    result = await service_user.change_password(
        current_password=change_password_data.current_password,
        password=change_password_data.password,
        user_info=current_user
    )

    if result == HTTPStatus.UNAUTHORIZED:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Invalid password'
        )

    if not result:
        raise HTTPException(
            status_code=HTTPStatus.BAD_GATEWAY,
            detail="Can't change password"
        )

    return result


@router.put(
    "/email",
    response_model=Status,
    status_code=HTTPStatus.ACCEPTED,
    summary="Cмена email",
    tags=['Пользователь']
)
async def change_email(
    params: ChangeEmail,
    current_user: UserInDB = Depends(get_current_user),
    service_user: UserService = Depends(user_service),
):
    if params.email == current_user.email:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='New email must be not equal past email'
        )
    result = await service_user.change_email(
        current_password=params.password,
        new_email=params.email,
        user_info=current_user
    )
    if result == HTTPStatus.CONFLICT:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Email already exist"
        )

    if result == HTTPStatus.UNAUTHORIZED:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Invalid password'
        )

    if not result:
        raise HTTPException(
            status_code=HTTPStatus.BAD_GATEWAY,
            detail="Can't change email"
        )
    return result
