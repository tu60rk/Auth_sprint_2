import pytest

from typing import Coroutine, Dict, Union

from ..settings import test_settings as sett
from ..testdata.users import (
    GETME_POSITIVE_DATA,
    CHANGE_PASSWORD_POSITIVE_DATA,
    CHANGE_EMAIL_POSITIVE_DATA
)


@pytest.mark.parametrize(
    'query_data, expected_answer',
    GETME_POSITIVE_DATA
)
@pytest.mark.anyio
async def test_positive_get_me(
    make_post_request: Coroutine,
    make_get_request_with_session: Coroutine,
    query_data: Dict[str, Union[str, int, float, None]],
    expected_answer: Dict[str, Union[str, int, float, None]],
):

    url = f'{sett.app_api_host}auth/login'
    response = await make_post_request(url, params=query_data)
    data_response = await response.json()

    url = f'{sett.app_api_host}users/me'
    response = await make_get_request_with_session(
        url,
        params={},
        headers={
            'Authorization': f'Bearer {data_response.get("access_token")}'
        }
    )
    data_response = await response.json()

    # check tests
    assert response.status == expected_answer.get('status')
    assert len(data_response) == expected_answer.get('length')
    assert data_response.get('email') == expected_answer.get('full_return').get('email')


@pytest.mark.parametrize(
    'query_data, expected_answer',
    GETME_POSITIVE_DATA
)
@pytest.mark.anyio
async def test_positive_get_account_history(
    make_post_request: Coroutine,
    make_get_request_with_session: Coroutine,
    query_data: Dict[str, Union[str, int, float, None]],
    expected_answer: Dict[str, Union[str, int, float, None]],
):
    pass


@pytest.mark.parametrize(
    'query_data, expected_answer',
    GETME_POSITIVE_DATA
)
@pytest.mark.anyio
async def test_negative_get_account_history(
    make_post_request: Coroutine,
    make_get_request_with_session: Coroutine,
    query_data: Dict[str, Union[str, int, float, None]],
    expected_answer: Dict[str, Union[str, int, float, None]],
):
    pass


@pytest.mark.parametrize(
    'query_data, expected_answer',
    CHANGE_PASSWORD_POSITIVE_DATA
)
@pytest.mark.anyio
async def test_positive_change_password(
    make_post_request: Coroutine,
    make_put_request_with_session: Coroutine,
    query_data: Dict[str, Union[str, int, float, None]],
    expected_answer: Dict[str, Union[str, int, float, None]],
):
    url = f'{sett.app_api_host}auth/login'
    response = await make_post_request(url, params=query_data)
    data_response = await response.json()

    url = f'{sett.app_api_host}users/password'
    response = await make_put_request_with_session(
        url,
        json={
            'current_password': query_data.get('current_password'),
            'password': query_data.get('new_password'),
            'repeat_password': query_data.get('repeat_password')
        },
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
    CHANGE_EMAIL_POSITIVE_DATA
)
@pytest.mark.anyio
async def test_positive_change_email(
    make_post_request: Coroutine,
    make_put_request_with_session: Coroutine,
    query_data: Dict[str, Union[str, int, float, None]],
    expected_answer: Dict[str, Union[str, int, float, None]],
):
    url = f'{sett.app_api_host}auth/login'
    response = await make_post_request(url, params=query_data)
    data_response = await response.json()

    url = f'{sett.app_api_host}users/email'
    response = await make_put_request_with_session(
        url,
        json={
            'email': query_data.get('new_email'),
            'password': query_data.get('password'),
        },
        headers={
            'Authorization': f'Bearer {data_response.get("access_token")}'
        }
    )
    data_response = await response.json()

    # check tests
    assert response.status == expected_answer.get('status')
    assert len(data_response) == expected_answer.get('length')
    assert data_response.get('status') == expected_answer.get('full_return').get('status')


