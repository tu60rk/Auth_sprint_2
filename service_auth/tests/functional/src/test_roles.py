import http
import pytest

from typing import Coroutine, Dict, Union

from ..settings import test_settings as sett
from ..testdata.roles import (
    GETROLES_POSITIVE_DATA,
    GETROLES_NEGATIVE_DATA,
    CREATEROLE_POSITIVE_DATA,
    CREATEROLE_NEGATIVE_DATA,
    CHANGEROLE_POSITIVE_DATA,
    CHANGEROLE_NEGATIVE_DATA,
    DELETEROLE_POSITIVE_DATA,
    DELETEROLE_NEGATIVE_DATA,
    SET_USER_ROLE_POSITIVE_DATA,
    SET_USER_ROLE_NEGATIVE_DATA,
    DELETE_USER_ROLE_POSITIVE_DATA
)


@pytest.mark.parametrize(
    'query_data, expected_answer',
    GETROLES_POSITIVE_DATA
)
@pytest.mark.anyio
async def test_positive_get_roles(
    make_post_request: Coroutine,
    make_get_request_with_session: Coroutine,
    query_data: Dict[str, Union[str, int, float, None]],
    expected_answer: Dict[str, Union[str, int, float, None]],
):

    url = f'{sett.app_api_host}auth/login'
    response = await make_post_request(url, params=query_data)
    data_response = await response.json()

    query_data = {}
    url = f'{sett.app_api_host}roles'
    response = await make_get_request_with_session(
        url,
        params=query_data,
        headers={
            'Authorization': f'Bearer {data_response.get("access_token")}'
        }
    )
    data_response = await response.json()

    # check tests
    assert response.status == expected_answer.get('status')
    assert len(data_response) == expected_answer.get('length')
    assert data_response[1].get('name') == expected_answer.get('full_return').get('admin')
    assert data_response[0].get('name') == expected_answer.get('full_return').get('user')


@pytest.mark.parametrize(
    'query_data, expected_answer',
    GETROLES_NEGATIVE_DATA
)
@pytest.mark.anyio
async def test_negative_getroles(
    make_get_request_with_session: Coroutine,
    query_data: Dict[str, Union[str, int, float, None]],
    expected_answer: Dict[str, Union[str, int, float, None]],
):
    query_data = {}
    url = f'{sett.app_api_host}roles'
    response = await make_get_request_with_session(
        url,
        params=query_data,
        headers={
            'Authorization': 'Bearer 123'
        }
    )
    data_response = await response.json()

    # check tests
    assert response.status == expected_answer.get('status')
    if response.status == http.HTTPStatus.UNPROCESSABLE_ENTITY:
        assert data_response.get('detail')[0].get('msg') == expected_answer.get('msg')
    else:
        assert data_response.get('detail') == expected_answer.get('msg')


@pytest.mark.parametrize(
    'query_data, expected_answer',
    CREATEROLE_POSITIVE_DATA
)
@pytest.mark.anyio
async def test_positive_create_role(
    make_post_request: Coroutine,
    make_post_request_with_session: Coroutine,
    query_data: Dict[str, Union[str, int, float, None]],
    expected_answer: Dict[str, Union[str, int, float, None]],
):

    url = f'{sett.app_api_host}auth/login'
    response = await make_post_request(url, params=query_data)
    data_response = await response.json()

    url = f'{sett.app_api_host}roles'
    response = await make_post_request_with_session(
        url,
        json=query_data,
        headers={
            'Authorization': f'Bearer {data_response.get("access_token")}'
        }
    )
    data_response = await response.json()

    # check tests
    assert response.status == expected_answer.get('status')
    assert len(data_response) == expected_answer.get('length')
    assert data_response.get('name') == expected_answer.get('full_return').get('name')


@pytest.mark.parametrize(
    'query_data, expected_answer',
    CREATEROLE_NEGATIVE_DATA
)
@pytest.mark.anyio
async def test_negative_create_role(
    make_post_request: Coroutine,
    make_post_request_with_session: Coroutine,
    query_data: Dict[str, Union[str, int, float, None]],
    expected_answer: Dict[str, Union[str, int, float, None]],
):

    url = f'{sett.app_api_host}auth/login'
    response = await make_post_request(url, params=query_data)
    data_response = await response.json()

    url = f'{sett.app_api_host}roles'
    response = await make_post_request_with_session(
        url,
        json=query_data,
        headers={
            'Authorization': f'Bearer {data_response.get("access_token")}'
        }
    )
    data_response = await response.json()

    # check tests
    assert response.status == expected_answer.get('status')
    if response.status == http.HTTPStatus.UNPROCESSABLE_ENTITY:
        assert data_response.get('detail')[0].get('msg') == expected_answer.get('msg')
    else:
        assert data_response.get('detail') == expected_answer.get('msg')


@pytest.mark.parametrize(
    'query_data, expected_answer',
    CHANGEROLE_POSITIVE_DATA
)
@pytest.mark.anyio
async def test_positive_change_role(
    make_post_request: Coroutine,
    make_put_request_with_session: Coroutine,
    query_data: Dict[str, Union[str, int, float, None]],
    expected_answer: Dict[str, Union[str, int, float, None]],
):

    url = f'{sett.app_api_host}auth/login'
    response = await make_post_request(url, params=query_data)
    data_response = await response.json()

    put_query_data = {
        'name': query_data.get('name'),
        'new_name': query_data.get('new_name'),
        'new_description': query_data.get('new_description')
    }
    url = f'{sett.app_api_host}roles'
    response = await make_put_request_with_session(
        url,
        params=put_query_data,
        headers={
            'Authorization': f'Bearer {data_response.get("access_token")}'
        }
    )
    data_response = await response.json()

    # check tests
    assert response.status == expected_answer.get('status')
    assert len(data_response) == expected_answer.get('length')
    assert data_response.get('status') == expected_answer.get('full_return').get('status')


@pytest.mark.parametrize(
    'query_data, expected_answer',
    CHANGEROLE_NEGATIVE_DATA
)
@pytest.mark.anyio
async def test_negative_change_role(
    make_post_request: Coroutine,
    make_put_request_with_session: Coroutine,
    query_data: Dict[str, Union[str, int, float, None]],
    expected_answer: Dict[str, Union[str, int, float, None]],
):

    url = f'{sett.app_api_host}auth/login'
    response = await make_post_request(url, params=query_data)
    data_response = await response.json()

    put_query_data = {
        'name': query_data.get('name'),
        'new_name': query_data.get('new_name'),
        'new_description': query_data.get('new_description')
    }
    url = f'{sett.app_api_host}roles'
    response = await make_put_request_with_session(
        url,
        params=put_query_data,
        headers={
            'Authorization': f'Bearer {data_response.get("access_token", None)}'
        }
    )
    data_response = await response.json()

    # check tests
    assert response.status == expected_answer.get('status')
    if response.status == http.HTTPStatus.UNPROCESSABLE_ENTITY:
        assert data_response.get('detail')[0].get('msg') == expected_answer.get('msg')
    else:
        assert data_response.get('detail') == expected_answer.get('msg')


@pytest.mark.parametrize(
    'query_data, expected_answer',
    DELETEROLE_POSITIVE_DATA
)
@pytest.mark.anyio
async def test_positive_delete_role(
    make_post_request: Coroutine,
    make_delete_request_with_session: Coroutine,
    query_data: Dict[str, Union[str, int, float, None]],
    expected_answer: Dict[str, Union[str, int, float, None]],
):

    url = f'{sett.app_api_host}auth/login'
    response = await make_post_request(url, params=query_data)
    data_response = await response.json()

    delete_query_data = {
        'name': query_data.get('name'),
    }
    url = f'{sett.app_api_host}roles'
    response = await make_delete_request_with_session(
        url,
        params=delete_query_data,
        headers={
            'Authorization': f'Bearer {data_response.get("access_token")}'
        }
    )
    data_response = await response.json()

    # check tests
    assert response.status == expected_answer.get('status')
    assert len(data_response) == expected_answer.get('length')
    assert data_response.get('status') == expected_answer.get('full_return').get('status')


@pytest.mark.parametrize(
    'query_data, expected_answer',
    DELETEROLE_NEGATIVE_DATA
)
@pytest.mark.anyio
async def test_negative_delete_role(
    make_post_request: Coroutine,
    make_delete_request_with_session: Coroutine,
    query_data: Dict[str, Union[str, int, float, None]],
    expected_answer: Dict[str, Union[str, int, float, None]],
):

    url = f'{sett.app_api_host}auth/login'
    response = await make_post_request(url, params=query_data)
    data_response = await response.json()

    delete_query_data = {
        'name': query_data.get('name', ''),
    }
    url = f'{sett.app_api_host}roles'
    response = await make_delete_request_with_session(
        url,
        params=delete_query_data,
        headers={
            'Authorization': f'Bearer {data_response.get("access_token", "")}'
        }
    )
    data_response = await response.json()

    # check tests
    assert response.status == expected_answer.get('status')
    if response.status == http.HTTPStatus.UNPROCESSABLE_ENTITY:
        assert data_response.get('detail')[0].get('msg') == expected_answer.get('msg')
    else:
        assert data_response.get('detail') == expected_answer.get('msg')


@pytest.mark.parametrize(
    'query_data, expected_answer',
    SET_USER_ROLE_POSITIVE_DATA
)
@pytest.mark.anyio
async def test_positive_set_user_role(
    make_post_request: Coroutine,
    make_post_request_with_session: Coroutine,
    query_data: Dict[str, Union[str, int, float, None]],
    expected_answer: Dict[str, Union[str, int, float, None]],
):

    url = f'{sett.app_api_host}auth/login'
    response = await make_post_request(url, params=query_data)
    data_response = await response.json()

    set_query_data = {
        'email': query_data.get('email'),
        'role_name': query_data.get('role_name'),
    }
    url = f'{sett.app_api_host}roles/user'
    response = await make_post_request_with_session(
        url,
        params=set_query_data,
        headers={
            'Authorization': f'Bearer {data_response.get("access_token")}'
        }
    )
    data_response = await response.json()

    # check tests
    assert response.status == expected_answer.get('status')
    assert len(data_response) == expected_answer.get('length')
    assert data_response == expected_answer.get('full_return')


@pytest.mark.parametrize(
    'query_data, expected_answer',
    SET_USER_ROLE_NEGATIVE_DATA
)
@pytest.mark.anyio
async def test_negative_set_user_role(
    make_post_request: Coroutine,
    make_post_request_with_session: Coroutine,
    query_data: Dict[str, Union[str, int, float, None]],
    expected_answer: Dict[str, Union[str, int, float, None]],
):

    url = f'{sett.app_api_host}auth/login'
    response = await make_post_request(url, params=query_data)
    data_response = await response.json()

    set_query_data = {
        'email': query_data.get('email'),
        'role_name': query_data.get('role_name'),
    }
    url = f'{sett.app_api_host}roles/user'
    response = await make_post_request_with_session(
        url,
        params=set_query_data,
        headers={
            'Authorization': f'Bearer {data_response.get("access_token")}'
        }
    )
    data_response = await response.json()

    # check tests
    assert response.status == expected_answer.get('status')
    if response.status == http.HTTPStatus.UNPROCESSABLE_ENTITY:
        assert data_response.get('detail')[0].get('msg') == expected_answer.get('msg')
    else:
        assert data_response.get('detail') == expected_answer.get('msg')


@pytest.mark.parametrize(
    'query_data, expected_answer',
    DELETE_USER_ROLE_POSITIVE_DATA
)
@pytest.mark.anyio
async def test_positive_delete_user_role(
    make_post_request: Coroutine,
    make_delete_request_with_session: Coroutine,
    query_data: Dict[str, Union[str, int, float, None]],
    expected_answer: Dict[str, Union[str, int, float, None]],
):

    url = f'{sett.app_api_host}auth/login'
    response = await make_post_request(url, params=query_data)
    data_response = await response.json()

    set_query_data = {
        'email': query_data.get('email'),
        'role_name': query_data.get('role_name'),
    }
    url = f'{sett.app_api_host}roles/user'
    response = await make_delete_request_with_session(
        url,
        params=set_query_data,
        headers={
            'Authorization': f'Bearer {data_response.get("access_token")}'
        }
    )
    data_response = await response.json()

    # check tests
    assert response.status == expected_answer.get('status')
    assert len(data_response) == expected_answer.get('length')
    assert data_response == expected_answer.get('full_return')