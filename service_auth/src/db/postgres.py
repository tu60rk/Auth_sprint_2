from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.sql import select, update, insert, delete

from src.models.entity import RefreshToken, Role, UserRoles
from src.core.config import settings

# Создаём движок
# Настройки подключения к БД передаём из переменных окружения, которые заранее загружены в файл настроек
engine = create_async_engine(
    settings.dsl_database,
    echo=True,
    future=True)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


class DbService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    @staticmethod
    def __prepare_select_sql_query(
        what_select,
        where_select: list = None,
        order_select=None,
        join_with=None,
    ):
        default_sql = select(what_select)
        if where_select:
            default_sql = default_sql.where(
                where_select[0] == where_select[1]
            )
        if order_select:
            default_sql = default_sql.order_by(order_select())
        if join_with:
            default_sql = default_sql.join(join_with)
        return default_sql

    @staticmethod
    def __prepare_update_sql_query(
        what_update,
        values_update: dict,
        where_update: list = None,
    ):
        default_sql = update(what_update)
        if where_update:
            default_sql = default_sql.where(
                where_update[0] == where_update[1]
            )
        return default_sql.values(**values_update)

    @staticmethod
    def __prepare_insert_sql_query(
        what_insert,
        values_insert: dict,
    ):
        default_sql = insert(what_insert)
        return default_sql.values(**values_insert)
    
    @staticmethod
    def __prepare_delete_sql_query(
        what_delete,
        where_delete: list = None,
    ):
        default_sql = delete(what_delete)
        if where_delete:
            default_sql = default_sql.where(
                where_delete[0] == where_delete[1]
            )
        return default_sql

    async def insert_data(self, data) -> None:
        self.db.add(data)
        await self.db.commit()
        await self.db.refresh(data)

    async def simple_select(
        self,
        what_select,
        where_select: list = None,
        order_select=None,
        join_with=None,
    ):

        sql = self.__prepare_select_sql_query(
            what_select=what_select,
            where_select=where_select,
            order_select=order_select,
            join_with=join_with,
        )

        data = await self.db.execute(sql)
        return [row for row in data.scalars()]

    async def simple_update(
        self,
        what_update,
        values_update: dict,
        where_update: list = None,
    ):
        sql = self.__prepare_update_sql_query(
            what_update=what_update,
            values_update=values_update,
            where_update=where_update
        )
        await self.db.execute(sql)
        await self.db.commit()

    async def update_token(
        self,
        what_update,
        values_update: dict,
        where_update: dict = None,
    ):

        await self.db.execute(
            update(what_update)
            .where(
                RefreshToken.user_agent == where_update['user_agent'],
                RefreshToken.user_id == where_update['user_id'],
                RefreshToken.is_active == where_update['is_active']
            )
            .values(values_update)
        )

        await self.db.commit()

    async def simple_insert(
        self,
        what_insert,
        values_insert: dict
    ):
        sql = self.__prepare_insert_sql_query(
            what_insert=what_insert,
            values_insert=values_insert
        )
        await self.db.execute(sql)
        await self.db.commit()

    async def simple_delete(
        self,
        what_delete,
        where_delete: list = None
    ):
        sql = self.__prepare_delete_sql_query(
            what_delete=what_delete,
            where_delete=where_delete
        )
        await self.db.execute(sql)
        await self.db.commit()

    async def get_user_roles(self, user_id) -> list:
        user_roles = await self.simple_select(
            what_select=Role.name,
            where_select=[UserRoles.user_id, user_id],
            join_with=UserRoles
        )
        return [role for role in user_roles]
