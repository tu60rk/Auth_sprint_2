from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from typing import List

from src.utils.oauth2 import get_current_user
from src.schemas.entity import Roles, UserInDB, Status
from src.services.roles import role_services, RolesService

router = APIRouter()


@router.post(
    "",
    response_model=Roles,
    status_code=HTTPStatus.ACCEPTED,
    summary="Создать роль",
    tags=["Роли"],
)
async def create_role(
    role: Roles,
    current_user: UserInDB = Depends(get_current_user),
    role_service: RolesService = Depends(role_services)
):
    role = await role_service.create_role(
        name=role.name,
        description=role.description
    )
    if role == HTTPStatus.BAD_REQUEST:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="This role exists"
        )

    if not role:
        raise HTTPException(
            status_code=HTTPStatus.BAD_GATEWAY,
            detail="Can't create role"
        )
    return role


@router.put(
    "",
    response_model=Status,
    status_code=HTTPStatus.ACCEPTED,
    summary="Изменить роль",
    tags=["Роли"],
)
async def change_role(
    name: str,
    new_name: str,
    new_description: str,
    current_user: UserInDB = Depends(get_current_user),
    role_service: RolesService = Depends(role_services)
):
    role = await role_service.change_role(
        name=name,
        new_name=new_name,
        new_description=new_description
    )
    if role == HTTPStatus.BAD_REQUEST:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="This role doesn't exist"
        )
    if not role:
        raise HTTPException(
            status_code=HTTPStatus.BAD_GATEWAY,
            detail="Can't change rolw"
        )
    return role


@router.get(
    "",
    response_model=List[Roles],
    status_code=HTTPStatus.ACCEPTED,
    summary="Получить роли",
    tags=["Роли"],
)
async def get_roles(
    current_user: UserInDB = Depends(get_current_user),
    role_service: RolesService = Depends(role_services)
):
    result = await role_service.get_roles()
    if not result:
        raise HTTPException(
            status_code=HTTPStatus.BAD_GATEWAY,
            detail="Can't change rolw"
        )
    return result


@router.delete(
    "",
    response_model=Status,
    status_code=HTTPStatus.ACCEPTED,
    summary="Удалить роль",
    tags=["Роли"],
)
async def delete_role(
    name: str,
    current_user: UserInDB = Depends(get_current_user),
    role_service: RolesService = Depends(role_services)
):
    role = await role_service.delete_role(
        name=name
    )
    if role == HTTPStatus.BAD_REQUEST:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="This role doesn't exist"
        )
    if not role:
        raise HTTPException(
            status_code=HTTPStatus.BAD_GATEWAY,
            detail="Can't delete role"
        )
    return role


@router.post(
    "/user",
    response_model=List[Roles],
    status_code=HTTPStatus.ACCEPTED,
    summary="Назначить роль пользователю",
    tags=["Роли"],
)
async def set_role_to_user(
    email: str,
    role_name: str,
    current_user: UserInDB = Depends(get_current_user),
    role_service: RolesService = Depends(role_services)
):
    role = await role_service.set_role_to_user(
        email=email,
        role_name=role_name
    )
    if role == HTTPStatus.BAD_REQUEST:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Role is not exist"
        )
    if role == HTTPStatus.CONFLICT:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="User is not exist"
        )

    if not role:
        raise HTTPException(
            status_code=HTTPStatus.BAD_GATEWAY,
            detail="Can't set a new role"
        )
    return role


@router.delete(
    "/user",
    response_model=Status,
    status_code=HTTPStatus.ACCEPTED,
    summary="Удалить роль у пользователя",
    tags=["Роли"],
)
async def delete_role_from_user(
    email: str,
    role_name: str,
    current_user: UserInDB = Depends(get_current_user),
    role_service: RolesService = Depends(role_services)
):
    role = await role_service.delete_role_to_user(
        email=email,
        role_name=role_name
    )
    if role == HTTPStatus.BAD_REQUEST:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Role is not exist"
        )
    if role == HTTPStatus.CONFLICT:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="User is not exist"
        )
    if not role:
        raise HTTPException(
            status_code=HTTPStatus.BAD_GATEWAY,
            detail="Can't delete a role for user"
        )
    return role
