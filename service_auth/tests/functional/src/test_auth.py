import http
import pytest

from typing import Coroutine, Dict, Union

from ..settings import test_settings as sett
from ..testdata.auth import (
    REGISTER_POSITIVE_DATA,
    REGISTER_NEGATIVE_DATA,
    LOGIN_POSITIVE_DATA,
    LOGIN_NEGATIVE_DATA,
    REFRESH_POSITIVE_DATA,
    REFRESH_NEGATIVE_DATA,
    LOGOUTME_POSITIVE_DATA,
    LOGOUTME_NEGATIVE_DATA,
    LOGOUTALL_POSITIVE_DATA,
    LOGOUTALL_NEGATIVE_DATA
)


@pytest.mark.parametrize(
    'query_data, expected_answer',
    REGISTER_POSITIVE_DATA
)
@pytest.mark.anyio
async def test_positive_register(
    make_post_request: Coroutine,
    query_data: Dict[str, Union[str, int, float, None]],
    expected_answer: Dict[str, Union[str, int, float, None]],
):

    url = f'{sett.app_api_host}auth/register'
    response = await make_post_request(url, params=query_data)
    data_response = await response.json()

    # check tests
    assert response.status == expected_answer.get('status')
    assert len(data_response) == expected_answer.get('length')
    assert data_response.get('email') == expected_answer.get('full_return').get('email')


@pytest.mark.parametrize(
    'query_data, expected_answer',
    REGISTER_NEGATIVE_DATA
)
@pytest.mark.anyio
async def test_negative_register(
    make_post_request: Coroutine,
    query_data: Dict[str, Union[str, int, float, None]],
    expected_answer: Dict[str, Union[str, int, float, None]],
):

    url = f'{sett.app_api_host}auth/register'
    response = await make_post_request(url, params=query_data)
    data_response = await response.json()

    # check tests
    assert response.status == expected_answer.get('status')
    if response.status == http.HTTPStatus.UNPROCESSABLE_ENTITY:
        assert data_response.get('detail')[0].get('msg') == expected_answer.get('msg')
    else:
        assert data_response.get('detail') == expected_answer.get('msg')


@pytest.mark.parametrize(
    'query_data, expected_answer',
    LOGIN_POSITIVE_DATA
)
@pytest.mark.anyio
async def test_positive_login(
    set_get_cache: Coroutine,
    make_post_request: Coroutine,
    query_data: Dict[str, Union[str, int, float, None]],
    expected_answer: Dict[str, Union[str, int, float, None]],
):

    url = f'{sett.app_api_host}auth/login'
    response = await make_post_request(url, params=query_data)
    data_response = await response.json()

    # check tests
    assert response.status == expected_answer.get('status')
    assert len(data_response) == expected_answer.get('length')

    access_token = data_response.get('access_token', None)
    refresh_token = data_response.get('refresh_token', None)
    assert access_token is not None
    assert refresh_token is not None

    # check redis
    data = await set_get_cache(key=access_token, value=refresh_token)
    assert data.decode('ascii') == refresh_token


@pytest.mark.parametrize(
    'query_data, expected_answer',
    LOGIN_NEGATIVE_DATA
)
@pytest.mark.anyio
async def test_negative_login(
    make_post_request: Coroutine,
    query_data: Dict[str, Union[str, int, float, None]],
    expected_answer: Dict[str, Union[str, int, float, None]],
):

    url = f'{sett.app_api_host}auth/login'
    response = await make_post_request(url, params=query_data)
    data_response = await response.json()
    # check tests
    assert response.status == expected_answer.get('status')
    if response.status == http.HTTPStatus.UNPROCESSABLE_ENTITY:
        assert data_response.get('detail')[0].get('msg') == expected_answer.get('msg')
    else:
        assert data_response.get('detail') == expected_answer.get('msg')


@pytest.mark.parametrize(
    'query_data, expected_answer',
    REFRESH_POSITIVE_DATA
)
@pytest.mark.anyio
async def test_positive_refresh(
    set_get_cache: Coroutine,
    make_post_request: Coroutine,
    query_data: Dict[str, Union[str, int, float, None]],
    expected_answer: Dict[str, Union[str, int, float, None]],
):

    url = f'{sett.app_api_host}auth/login'
    response = await make_post_request(url, params=query_data)
    data_response = await response.json()

    query_data = {'refresh_token': data_response.get('refresh_token', None)}
    url = f'{sett.app_api_host}auth/refresh'
    response = await make_post_request(url, params=query_data)
    data_response = await response.json()

    # check tests
    assert response.status == expected_answer.get('status')
    assert len(data_response) == expected_answer.get('length')
    access_token = data_response.get('access_token', None)
    refresh_token = data_response.get('refresh_token', None)
    assert access_token is not None
    assert refresh_token is not None

    # check redis
    data = await set_get_cache(key=access_token, value=refresh_token)
    assert data.decode('ascii') == refresh_token


@pytest.mark.parametrize(
    'query_data, expected_answer',
    REFRESH_NEGATIVE_DATA
)
@pytest.mark.anyio
async def test_negative_refresh(
    make_post_request: Coroutine,
    query_data: Dict[str, Union[str, int, float, None]],
    expected_answer: Dict[str, Union[str, int, float, None]],
):

    url = f'{sett.app_api_host}auth/refresh'
    response = await make_post_request(url, params=query_data)
    data_response = await response.json()
    # check tests
    assert response.status == expected_answer.get('status')
    if response.status == http.HTTPStatus.UNPROCESSABLE_ENTITY:
        assert data_response.get('detail')[0].get('msg') == expected_answer.get('msg')
    else:
        assert data_response.get('detail') == expected_answer.get('msg')


@pytest.mark.parametrize(
    'query_data, expected_answer',
    LOGOUTME_POSITIVE_DATA
)
@pytest.mark.anyio
async def test_positive_logoutme(
    make_post_request_with_session: Coroutine,
    make_post_request: Coroutine,
    query_data: Dict[str, Union[str, int, float, None]],
    expected_answer: Dict[str, Union[str, int, float, None]],
):

    url = f'{sett.app_api_host}auth/login'
    response = await make_post_request(url, params=query_data)
    data_response = await response.json()

    query_data = {}
    url = f'{sett.app_api_host}auth/logout/me'
    response = await make_post_request_with_session(url, json=query_data, headers={'Authorization': f'Bearer {data_response.get("access_token")}'})
    data_response = await response.json()

    # check tests
    assert response.status == expected_answer.get('status')
    assert len(data_response) == expected_answer.get('length')


@pytest.mark.parametrize(
    'query_data, expected_answer',
    LOGOUTME_NEGATIVE_DATA
)
@pytest.mark.anyio
async def test_negative_logoutme(
    make_post_request_with_session: Coroutine,
    make_post_request: Coroutine,
    query_data: Dict[str, Union[str, int, float, None]],
    expected_answer: Dict[str, Union[str, int, float, None]],
):

    url = f'{sett.app_api_host}auth/login'
    response = await make_post_request(url, params=query_data)
    data_response = await response.json()

    query_data = {}
    url = f'{sett.app_api_host}auth/logout/me'
    response = await make_post_request_with_session(url, json=query_data, headers={'Authorization': f'Bearer {data_response.get("access_token")}'})
    data_response = await response.json()

    assert response.status == expected_answer.get('status')
    if response.status == http.HTTPStatus.UNPROCESSABLE_ENTITY:
        assert data_response.get('detail')[0].get('msg') == expected_answer.get('msg')
    else:
        assert data_response.get('detail') == expected_answer.get('msg')


@pytest.mark.parametrize(
    'query_data, expected_answer',
    LOGOUTALL_POSITIVE_DATA
)
@pytest.mark.anyio
async def test_positive_logoutall(
    make_post_request_with_session: Coroutine,
    make_post_request: Coroutine,
    query_data: Dict[str, Union[str, int, float, None]],
    expected_answer: Dict[str, Union[str, int, float, None]],
):

    url = f'{sett.app_api_host}auth/login'
    response = await make_post_request(url, params=query_data)
    data_response = await response.json()

    query_data = {}
    url = f'{sett.app_api_host}auth/logout/all'
    response = await make_post_request_with_session(url, json=query_data, headers={'Authorization': f'Bearer {data_response.get("access_token")}'})
    data_response = await response.json()

    # check tests
    assert response.status == expected_answer.get('status')
    assert len(data_response) == expected_answer.get('length')


@pytest.mark.parametrize(
    'query_data, expected_answer',
    LOGOUTALL_NEGATIVE_DATA
)
@pytest.mark.anyio
async def test_negative_logoutall(
    make_post_request_with_session: Coroutine,
    make_post_request: Coroutine,
    query_data: Dict[str, Union[str, int, float, None]],
    expected_answer: Dict[str, Union[str, int, float, None]],
):

    url = f'{sett.app_api_host}auth/login'
    response = await make_post_request(url, params=query_data)
    data_response = await response.json()

    query_data = {}
    url = f'{sett.app_api_host}auth/logout/me'
    response = await make_post_request_with_session(url, json=query_data, headers={'Authorization': f'Bearer {data_response.get("access_token")}'})
    data_response = await response.json()

    assert response.status == expected_answer.get('status')
    if response.status == http.HTTPStatus.UNPROCESSABLE_ENTITY:
        assert data_response.get('detail')[0].get('msg') == expected_answer.get('msg')
    else:
        assert data_response.get('detail') == expected_answer.get('msg')
