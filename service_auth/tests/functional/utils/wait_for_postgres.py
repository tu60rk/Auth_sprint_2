import asyncio
import asyncpg

from tests.functional.settings import test_settings as sett
from tests.functional.utils.helpers import backoff


@backoff(start_sleep_time=1, factor=2, border_sleep_time=20)
async def main():

    conn = await asyncpg.connect(
        host=sett.db_host,
        port=sett.db_port,
        user=sett.db_user,
        password=sett.db_password,
        database=sett.db_name
    )
    await conn.execute('select 1')


if __name__ == '__main__':
    asyncio.run(main())
