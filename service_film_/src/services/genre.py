from functools import lru_cache
from typing import Optional, List

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic, ElasticAsyncSearchEngine
from models.film import Genres
from services.abstracts import AsyncSearchEngine, BasicService


class GenreService(BasicService):
    INDEX = 'genres'

    def __init__(self, search_engine: AsyncSearchEngine) -> None:
        self.search_engine = search_engine

    async def get_by_search(
        self,
        query: str,
        page_size: int,
        page_number: int,
    ) -> Optional[List[Genres]]:
        query = self.search_engine.prepare_query(
            type='genres_by_query',
            values=[query]
        ),
        result = await self.search_engine.search(
            index=self.INDEX,
            query=query,
            from_=page_number,
            size=page_size,
            sort='_score',
        )
        if result is None:
            return None

        return [
            Genres(
                id=row['_source'].get('id'),
                name=row['_source'].get('name'),
                description=row['_source'].get('description'),
            )
            for row in result['hits']['hits']
        ]

    async def get_all(
        self,
        page_size: int,
        page_number: int,
    ) -> Optional[List[Genres]]:
        result = await self.search_engine.search(
            index=self.INDEX,
            query=self.search_engine.prepare_query(type='all'),
            from_=page_number,
            size=page_size,
        )
        if result is None:
            return None

        return [
            Genres(
                **row['_source'],
            )
            for row in result['hits']['hits']
        ]

    async def get_by_id(self, genre_id: str) -> Optional[Genres]:
        doc = await self.search_engine.get_by_id(
            index=self.INDEX,
            _id=genre_id
        )
        if doc is None:
            return None
        return Genres(**doc['_source'])


@lru_cache()
def get_genre_service(
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    search_engine = ElasticAsyncSearchEngine(elastic=elastic)
    return GenreService(search_engine=search_engine)
