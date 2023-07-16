from functools import lru_cache
from typing import Optional, List
import uuid

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic, ElasticAsyncSearchEngine
from models.film import Film, Films
from services.abstracts import AsyncSearchEngine, BasicService


class FilmService(BasicService):
    INDEX = 'movies'

    def __init__(self, search_engine: AsyncSearchEngine) -> None:
        self.search_engine = search_engine

    async def get_by_search(
        self,
        query: str,
        page_size: int,
        page_number: int
    ) -> Optional[List[Films]]:
        query = self.search_engine.prepare_query(
            type='films_by_query',
            values=[query]
        )
        films = await self.search_engine.search(
            index=self.INDEX,
            query=query,
            from_=page_number,
            size=page_size,
            sort='_score'
        )
        if films is None:
            return None
        return [Films(
                id=row['_source'].get('id'),
                title=row['_source'].get('title'),
                imdb_raiting=row['_source'].get('imdb_raiting')
                ) for row in films["hits"]["hits"]]

    async def get_all(self,
                      genre: uuid.UUID,
                      sort_param: str,
                      page_size: int,
                      page_number: int
                      ) -> Optional[List[Films]]:
        sorting = self.search_engine.prepare_sorting(sort_param=sort_param)

        type = 'films_by_genre' if genre else 'all'
        values = [genre] if genre else []
        query = self.search_engine.prepare_query(type=type, values=values)

        result = await self.search_engine.search(
            index=self.INDEX,
            from_=page_number,
            size=page_size,
            query=query,
            sort=sorting
        )
        if result is None:
            return None
        return [Films(
                id=row['_source'].get('id'),
                title=row['_source'].get('title'),
                imdb_raiting=row['_source'].get('imdb_raiting')
                ) for row in result["hits"]["hits"]]

    async def get_by_id(self, film_id: uuid.UUID) -> Optional[Film]:
        film = await self.search_engine.get_by_id(
            index=self.INDEX,
            _id=film_id
        )
        if film is None:
            return None
        return Film(
            id=film['_source'].get('id'),
            title=film['_source'].get('title'),
            description=film['_source'].get('description'),
            imdb_raiting=film['_source'].get('imdb_raiting'),
            genres=film['_source'].get('genres'),
            actors=film['_source'].get('actors'),
            writers=film['_source'].get('writers'),
            directors=film['_source'].get('directors')
        )


@lru_cache()
def get_film_service(
    elastic: AsyncElasticsearch = Depends(get_elastic)
) -> FilmService:
    search_engine = ElasticAsyncSearchEngine(elastic=elastic)
    return FilmService(search_engine=search_engine)
