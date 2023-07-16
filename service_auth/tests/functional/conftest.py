import pytest
import aiohttp

from redis.asyncio import Redis

from .settings import test_settings as sett


@pytest.fixture(scope='session')
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope='session')
async def http_client():
    async with aiohttp.ClientSession() as client:
        yield client


@pytest.fixture(scope='function')
def make_get_request_with_session():
    async def inner(query: str, params: dict, headers: dict= {}):
        async with aiohttp.ClientSession(headers=headers) as client:
            response = await client.get(query, params=params)
        return response
    return inner


@pytest.fixture(scope='function')
def make_post_request_with_session():
    async def inner(query: str, params: dict = {}, headers: dict= {}, json: dict = {}):
        async with aiohttp.ClientSession(headers=headers) as client:
            response = await client.post(query, json=json, params=params)
        return response
    return inner


@pytest.fixture(scope='function')
def make_post_request(http_client: aiohttp.ClientSession):
    async def inner(query: str, params: dict):
        response = await http_client.post(query, json=params)
        return response
    return inner


@pytest.fixture(scope='function')
def make_put_request_with_session(http_client: aiohttp.ClientSession):
    async def inner(query: str, params: dict = {}, headers: dict = {}, json: dict = {}):
        async with aiohttp.ClientSession(headers=headers) as client:
            response = await client.put(query, params=params, json=json)
        return response
    return inner


@pytest.fixture(scope='function')
def make_delete_request_with_session(http_client: aiohttp.ClientSession):
    async def inner(query: str, params: dict, headers: dict= {}):
        async with aiohttp.ClientSession(headers=headers) as client:
            response = await client.delete(query, params=params)
        return response
    return inner


@pytest.fixture(scope='function')
def set_get_cache():
    async def inner(key: str, value: str):
        client = Redis(
            host=sett.redis_host,
            port=sett.redis_port,
            db=sett.redis_db_test
        )
        await client.set(key, value)
        data = await client.get(key)
        return data
    return inner
