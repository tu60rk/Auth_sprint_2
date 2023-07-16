from typing import Optional, Any
from elasticsearch import AsyncElasticsearch, NotFoundError
from db.elastic_queries import (
    FIND_FILMS_BY_GENRE,
    FIND_FILMS_BY_QUERY,
    FIND_FILMS_BY_PERSON,
    FIND_ALL,
    FIND_PERSONS_BY_QUERY,
    FIND_FILMS_BY_PERSONS
)
from services.abstracts import AsyncSearchEngine


es: Optional[AsyncElasticsearch] = None


# Функция понадобится при внедрении зависимостей
async def get_elastic() -> Optional[AsyncElasticsearch]:
    return es


class ElasticAsyncSearchEngine(AsyncSearchEngine):

    def __init__(self, elastic: AsyncElasticsearch) -> None:
        self.elastic = elastic

    async def get_by_id(self, index: str, _id: str) -> Any:
        try:
            return await self.elastic.get(index=index, id=_id)
        except NotFoundError:
            return None

    async def search(
        self,
        index: str,
        query: dict,
        from_: int = None,
        size: int = None,
        sort: str = None
    ) -> Any:
        try:
            return await self.elastic.search(
                    index=index,
                    from_=from_,
                    size=size,
                    query=query,
                    sort=sort
                )
        except NotFoundError:
            return None

    @staticmethod
    def prepare_sorting(sort_param: str) -> str:
        if sort_param[0] == '-':
            type_sort = ':desc'
        elif sort_param[0] == '+':
            type_sort = ':asc'
        else:
            type_sort = ':desc'

        return f'{sort_param[1:]}{type_sort}'

    @staticmethod
    def prepare_query(type: str, values: list = None) -> dict:
        if type == 'films_by_genre':
            FIND_FILMS_BY_GENRE['nested']['query']['bool']['must'][0]['match']['genres.id'] = values[0]
            return FIND_FILMS_BY_GENRE
        if type == 'films_by_query':
            FIND_FILMS_BY_QUERY['multi_match']['query'] = values[0]
            return FIND_FILMS_BY_QUERY
        if type == 'films_by_person':
            FIND_FILMS_BY_PERSON['bool']['should'][0]['nested']['query']['bool']['must'][0]['match']['actors.id'] = values[0]
            FIND_FILMS_BY_PERSON['bool']['should'][1]['nested']['query']['bool']['must'][0]['match']['writers.id'] = values[0]
            FIND_FILMS_BY_PERSON['bool']['should'][2]['nested']['query']['bool']['must'][0]['match']['directors.id'] = values[0]
            return FIND_FILMS_BY_PERSON
        if type == 'persons_by_query':
            FIND_PERSONS_BY_QUERY['multi_match']['query'] = values[0]
            return FIND_PERSONS_BY_QUERY
        if type == 'films_by_persons':
            FIND_FILMS_BY_PERSONS['bool']['should'][0]['nested']['query']['terms']['actors.id'] = values
            FIND_FILMS_BY_PERSONS['bool']['should'][1]['nested']['query']['terms']['writers.id'] = values
            FIND_FILMS_BY_PERSONS['bool']['should'][2]['nested']['query']['terms']['directors.id'] = values
            return FIND_FILMS_BY_PERSONS
        if type == 'all':
            return FIND_ALL
