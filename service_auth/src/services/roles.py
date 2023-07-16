from http import HTTPStatus
from functools import lru_cache
from typing import List, Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select, delete

from src.db.postgres import get_session, DbService
from src.schemas.entity import Roles, Status
from src.models.entity import Role, User, UserRoles


class RolesService:
    def __init__(self, db_service: DbService) -> None:
        self.db_service = db_service

    async def _check_role_by_name(self, name: str) -> bool:
        role_exist = await self.db_service.simple_select(
            what_select=Role,
            where_select=[Role.name, name]
        )
        if len(role_exist) > 0:
            return role_exist[0]
        return False

    async def _check_user_by_email(self, email: str) -> bool:
        existing_user = await self.db_service.simple_select(
            what_select=User,
            where_select=[User.email, email]
        )
        if len(existing_user) > 0:
            return existing_user[0]
        return False

    async def create_role(
        self,
        name: str,
        description: str
    ) -> Optional[Roles]:

        try:
            role_exist = await self._check_role_by_name(name=name)
            if role_exist:
                return HTTPStatus.BAD_REQUEST

            await self.db_service.simple_insert(
                what_insert=Role,
                values_insert={
                    "name": name,
                    "description": description
                }
            )
        except Exception:
            return None
        return Roles(name=name, description=description)

    async def change_role(
        self,
        name: str,
        new_description: str,
        new_name: str,
    ) -> Optional[Status]:

        try:
            role_exist = await self._check_role_by_name(name=name)
            if not role_exist:
                return HTTPStatus.BAD_REQUEST

            values = {"description": new_description}
            values.update({'name': new_name}) if new_name else ''
            await self.db_service.simple_update(
                what_update=Role,
                where_update=[Role.name, name],
                values_update=values
            )
        except Exception:
            return None
        return Status(status='success')

    async def get_roles(self) -> List[Roles]:
        try:
            datas = await self.db_service.simple_select(Role)
            return [
                Roles(name=data.name, description=data.description)
                for data in datas
            ]
        except Exception:
            return None

    async def delete_role(self, name: str) -> Optional[Status]:
        try:
            role_exist = await self._check_role_by_name(name=name)
            if not role_exist:
                return HTTPStatus.BAD_REQUEST
            await self.db_service.simple_delete(
                what_delete=Role,
                where_delete=[Role.name, name]
            )
            return Status(status='success')
        except Exception:
            return None

    async def set_role_to_user(
        self,
        email: str,
        role_name: str,
    ) -> Optional[Roles]:

        try:
            role_exist = await self._check_role_by_name(name=role_name)
            if not role_exist:
                return HTTPStatus.BAD_REQUEST
            existing_user = await self._check_user_by_email(email=email)
            if not existing_user:
                return HTTPStatus.CONFLICT

            user_roles = await self.db_service.db.execute(
                select(UserRoles)
                .where(
                    UserRoles.user_id == existing_user.id,
                    UserRoles.role_id == role_exist.id
                )
            )
            if user_roles.scalar():
                user_roles = await self.db_service.simple_select(
                    what_select=Role,
                    where_select=[UserRoles.user_id, existing_user.id],
                    join_with=UserRoles
                )
                return [
                    Roles(name=role.name, description=role.description)
                    for role in user_roles
                ]

            data_insert = UserRoles(
                user_id=existing_user.id,
                role_id=role_exist.id
            )

            await self.db_service.insert_data(data_insert)
            user_roles = await self.db_service.simple_select(
                what_select=Role,
                where_select=[UserRoles.user_id, existing_user.id],
                join_with=UserRoles
            )

            return [
                Roles(name=role.name, description=role.description) 
                for role in user_roles
            ]
        except Exception:
            return None

    async def delete_role_to_user(
        self,
        email: str,
        role_name: str,
    ) -> Optional[Status]:

        try:
            role_exist = await self._check_role_by_name(name=role_name)
            if not role_exist:
                return HTTPStatus.BAD_REQUEST
            existing_user = await self._check_user_by_email(email=email)
            if not existing_user:
                return HTTPStatus.CONFLICT

            await self.db_service.db.execute(
                delete(UserRoles)
                .where(
                    UserRoles.user_id == existing_user.id,
                    UserRoles.role_id == role_exist.id
                )
            )
            await self.db_service.db.commit()
            return Status(status='success')
        except Exception:
            return None


@lru_cache()
def role_services(
    db: AsyncSession = Depends(get_session),
) -> RolesService:
    return RolesService(
        db_service=DbService(db=db)
    )
