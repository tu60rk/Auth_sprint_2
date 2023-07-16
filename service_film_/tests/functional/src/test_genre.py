import pytest
import json

from typing import Coroutine, Dict, Union

from ..settings import test_settings as sett
from ..testdata.genre import (
    ES_GENRE_GEN_DATA,
    ES_GENRES_PARAMETRIZE_POSITIVE_DATA,
    ES_GENRES_PARAMETRIZE_NEGATIVE_DATA,
    ES_GENRE_BY_ID_PARAMETRIZE_POSITIVE_DATA,
    ES_GENRE_BY_ID_PARAMETRIZE_NEGATIVE_DATA
)


@pytest.mark.parametrize(
    'query_data, expected_answer',
    ES_GENRES_PARAMETRIZE_POSITIVE_DATA
)
@pytest.mark.anyio
async def test_positive_get_all_genres(
    make_get_request: Coroutine,
    es_write_data: Coroutine,
    set_get_cache,
    query_data: Dict[str, Union[str, int, float, None]],
    expected_answer: Dict[str, Union[str, int, float, None]],
):

    await es_write_data(data=ES_GENRE_GEN_DATA, index='genres')

    url = f'{sett.app_api_host}genres'
    response = await make_get_request(url, params=query_data)
    data_response = await response.json()

    assert response.status == expected_answer.get('status')
    assert len(data_response) == expected_answer.get('length')
    assert data_response[0].get('name') == expected_answer.get('full_return').get('name')
    assert data_response[0].get('description') == expected_answer.get('full_return').get('description')

    # test redis
    key_ = expected_answer.get('full_return').get('id')
    value = expected_answer.get('full_return')
    response = set_get_cache(key=key_, value=json.dumps(value))
    assert value == json.loads(response)


@pytest.mark.parametrize(
    'query_data, expected_answer',
    ES_GENRES_PARAMETRIZE_NEGATIVE_DATA
)
@pytest.mark.anyio
async def test_negative_get_all_genres(
    make_get_request: Coroutine,
    es_write_data: Coroutine,
    query_data: Dict[str, Union[str, int, float, None]],
    expected_answer: Dict[str, Union[str, int, float, None]],
):

    await es_write_data(data=ES_GENRE_GEN_DATA, index='genres')

    url = f'{sett.app_api_host}genres'
    response = await make_get_request(url, params=query_data)
    data_response = await response.json()

    assert response.status == expected_answer.get('status')
    assert len(data_response) == expected_answer.get('length')
    assert data_response.get('detail')[0].get('msg') == expected_answer.get('msg')


@pytest.mark.parametrize(
    ('genre_id', 'expected_answer'),
    ES_GENRE_BY_ID_PARAMETRIZE_POSITIVE_DATA
)
@pytest.mark.anyio
async def test_positive_get_genre_by_id(
    make_get_request: Coroutine,
    es_write_data: Coroutine,
    set_get_cache,
    genre_id: Dict[str, Union[str, int, float, None]],
    expected_answer: Dict[str, Union[str, int, float, None]]
):

    await es_write_data(data=ES_GENRE_GEN_DATA, index='genres')

    url = f'{sett.app_api_host}genres/{genre_id.get("genre_id")}'
    response = await make_get_request(url, '')
    data_response = await response.json()

    assert response.status == expected_answer.get('status')
    assert len(data_response) == expected_answer.get('length')
    assert data_response['name'] == expected_answer.get('full_return').get('name')
    assert data_response['description'] == expected_answer.get('full_return').get('description')

    # test redis
    key_ = expected_answer.get('full_return').get('id')
    value = expected_answer.get('full_return')
    response = set_get_cache(key=key_, value=json.dumps(value))
    assert value == json.loads(response)

@pytest.mark.parametrize(
    ('genre_id', 'expected_answer'),
    ES_GENRE_BY_ID_PARAMETRIZE_NEGATIVE_DATA
)
@pytest.mark.anyio
async def test_negative_get_genre_by_id(
    make_get_request: Coroutine,
    es_write_data: Coroutine,
    genre_id: Dict[str, Union[str, int, float, None]],
    expected_answer: Dict[str, Union[str, int, float, None]]
):

    await es_write_data(data=ES_GENRE_GEN_DATA, index='genres')

    url = f'{sett.app_api_host}genres/{genre_id.get("genre_id")}'
    response = await make_get_request(url, '')
    data_response = await response.json()

    assert response.status == expected_answer.get('status')
    assert len(data_response) == expected_answer.get('length')
    assert data_response['detail'][0].get('msg') == expected_answer.get('msg')
