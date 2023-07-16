import pytest
import json

from typing import Coroutine, Dict, Union

from ..settings import test_settings as sett
from ..testdata.genre import ES_GENRE_GEN_DATA
from ..testdata.film import (
    UUIDS_FILMS,
    ES_FILM_SEARCH_GEN_DATA,
    ES_FILMS_PARAMETRIZE_POSITIVE_DATA,
    ES_FILMS_PARAMETRIZE_NEGATIVE_DATA,
    ES_FILM_BY_ID_PARAMETRIZE_POSITIVE_DATA,
    ES_FILM_BY_ID_PARAMETRIZE_NEGATIVE_DATA
)


@pytest.mark.parametrize(
    'query_data, expected_answer',
    ES_FILMS_PARAMETRIZE_POSITIVE_DATA
)
@pytest.mark.anyio
async def test_positive_get_all_films(
    make_get_request: Coroutine,
    es_write_data: Coroutine,
    set_get_cache,
    query_data: Dict[str, Union[str, int, float, None]],
    expected_answer: Dict[str, Union[str, int, float, None]],
):

    # load data into es
    es_data = []
    for film_id in UUIDS_FILMS:
        ES_FILM_SEARCH_GEN_DATA['id'] = film_id
        es_data.append(ES_FILM_SEARCH_GEN_DATA.copy())

    await es_write_data(data=es_data, index='movies')
    await es_write_data(data=ES_GENRE_GEN_DATA, index='genres')

    # make a request
    url = f'{sett.app_api_host}films'
    response = await make_get_request(url, params=query_data)
    data_response = await response.json()

    # check tests
    assert response.status == expected_answer.get('status')
    assert len(data_response) == expected_answer.get('length')
    assert data_response[0].get('title') == expected_answer.get('full_return')[0].get('title')
    assert data_response[0].get('imdb_raiting') == expected_answer.get('full_return')[0].get('imdb_raiting')

    # test redis
    key_ = expected_answer.get('full_return')[0].get('id')
    value = expected_answer.get('full_return')[0]
    response = set_get_cache(key=key_, value=json.dumps(value))
    assert value == json.loads(response)


@pytest.mark.parametrize(
    'query_data, expected_answer',
    ES_FILMS_PARAMETRIZE_NEGATIVE_DATA
)
@pytest.mark.anyio
async def test_negative_get_all_films(
    make_get_request: Coroutine,
    es_write_data: Coroutine,
    query_data: Dict[str, Union[str, int, float, None]],
    expected_answer: Dict[str, Union[str, int, float, None]],
):

    # load data into es
    es_data = []
    for film_id in UUIDS_FILMS:
        ES_FILM_SEARCH_GEN_DATA['id'] = film_id
        es_data.append(ES_FILM_SEARCH_GEN_DATA.copy())

    await es_write_data(data=es_data, index='movies')
    await es_write_data(data=ES_GENRE_GEN_DATA, index='genres')

    # make a request
    url = f'{sett.app_api_host}films'
    response = await make_get_request(url, params=query_data)
    data_response = await response.json()

    # check tests
    assert response.status == expected_answer.get('status')
    assert len(data_response) == expected_answer.get('length')
    assert data_response.get('detail')[0].get('msg') == expected_answer.get('msg')


@pytest.mark.parametrize(
    'query_data, expected_answer',
    ES_FILM_BY_ID_PARAMETRIZE_POSITIVE_DATA
)
@pytest.mark.anyio
async def test_positive_film_by_id(
    make_get_request: Coroutine,
    es_write_data: Coroutine,
    set_get_cache,
    query_data: Dict[str, Union[str, int, float, None]],
    expected_answer: Dict[str, Union[str, int, float, None]],
):

    # load data into es
    es_data = []
    for film_id in UUIDS_FILMS:
        ES_FILM_SEARCH_GEN_DATA['id'] = film_id
        es_data.append(ES_FILM_SEARCH_GEN_DATA.copy())

    await es_write_data(data=es_data, index='movies')

    # make a request
    url = f'{sett.app_api_host}films/{query_data.get("film_id")}'
    response = await make_get_request(url, '')
    data_response = await response.json()

    # check tests
    assert response.status == expected_answer.get('status')
    assert len(data_response) == expected_answer.get('length')
    assert data_response.get('title') == expected_answer.get('full_return').get('title')
    assert data_response.get('imdb_raiting') == expected_answer.get('full_return').get('imdb_raiting')

    # test redis
    key_ = expected_answer.get('full_return').get('id')
    value = expected_answer.get('full_return')
    response = set_get_cache(key=key_, value=json.dumps(value))
    assert value == json.loads(response)


@pytest.mark.parametrize(
    'query_data, expected_answer',
    ES_FILM_BY_ID_PARAMETRIZE_NEGATIVE_DATA
)
@pytest.mark.anyio
async def test_negative_film_by_id(
    make_get_request: Coroutine,
    es_write_data: Coroutine,
    query_data: Dict[str, Union[str, int, float, None]],
    expected_answer: Dict[str, Union[str, int, float, None]],
):

    # load data into es
    es_data = []
    for film_id in UUIDS_FILMS:
        ES_FILM_SEARCH_GEN_DATA['id'] = film_id
        es_data.append(ES_FILM_SEARCH_GEN_DATA.copy())

    await es_write_data(data=es_data, index='movies')

    # make a request
    url = f'{sett.app_api_host}films/{query_data.get("film_id")}'
    response = await make_get_request(url, '')
    data_response = await response.json()

    # check tests
    assert response.status == expected_answer.get('status')
    assert len(data_response) == expected_answer.get('length')
    assert data_response.get('detail')[0].get('msg') == expected_answer.get('msg')