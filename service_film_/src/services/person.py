from functools import lru_cache
from typing import Optional, List, Dict
import uuid

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic, ElasticAsyncSearchEngine
from models.film import Films
from models.person import Person
from services.abstracts import AsyncSearchEngine, BasicService


class PersonService(BasicService):
    INDEX = 'persons'

    def __init__(self, search_engine: AsyncSearchEngine) -> None:
        self.search_engine = search_engine

    async def get_by_search(
        self,
        query: str,
        page_size: int,
        page_number: int,
    ) -> Optional[List[Person]]:
        query = self.search_engine.prepare_query(
            type='persons_by_query',
            values=[query]
        )
        persons = await self.search_engine.search(
            index=self.INDEX,
            query=query,
            from_=page_number,
            size=page_size,
            sort='_score',
        )

        person_ids = [
            str(
                row['_source'].get('id')
            ) for row in persons["hits"]["hits"]
        ]
        if len(person_ids):
            query = self.search_engine.prepare_query(
                type='films_by_persons',
                values=person_ids
            )
            films = await self.search_engine.search(
                index='movies',
                query=query,
            )

            result = []
            for per in persons["hits"]["hits"]:

                per_id = per['_source'].get('id')
                full_name = per['_source'].get('full_name')
                new_films = self._create_roles_list(
                        person_id=per_id,
                        source=films['hits']['hits']
                    )

                result.append(Person(
                    uuid=per_id,
                    full_name=full_name,
                    films=new_films,
                ))
            return result
        return None

    async def get_by_id(self, person_id: uuid.UUID) -> Optional[Person]:
        doc = await self.search_engine.get_by_id(
            index=self.INDEX,
            _id=person_id
        )
        if doc is None:
            return None
        person_id = doc['_source'].get('id', None)
        full_name = doc['_source'].get('full_name', None)
        films = await self.find_films_roles(person_id=person_id)
        return Person(
            uuid=person_id,
            full_name=full_name,
            films=films,
        )

    async def find_films_roles(
        self,
        person_id: uuid.UUID
    ) -> Optional[List[Dict[uuid.UUID, List[str]]]]:

        query = self.search_engine.prepare_query(
            type='films_by_person',
            values=[person_id]
        )
        search_films = await self.search_engine.search(
                index='movies',
                query=query,
            )
        films = self._create_roles_list(
            person_id=person_id,
            source=search_films['hits']['hits']
        )
        return films

    async def get_films_by_person_id(
        self,
        person_id: uuid.UUID,
        page_size: int,
        page_number: int,
    ) -> Optional[List[Films]]:
        query = self.search_engine.prepare_query(
            type='films_by_person',
            values=[person_id]
        )
        films = await self.search_engine.search(
            index='movies',
            query=query,
            from_=page_number,
            size=page_size,
        )
        if films is None:
            return None
        return [Films(
                id=row['_source'].get('id'),
                title=row['_source'].get('title'),
                imdb_raiting=row['_source'].get('imdb_raiting'),
                ) for row in films['hits']['hits']]

    @staticmethod
    def _create_roles_list(
        person_id: uuid.UUID,
        source: List[str]
    ) -> List[str]:

        abstract_list = []
        for row in source:
            roles = []
            if person_id in [
                person.get('id') for person in row['_source'].get('directors')
            ]:
                roles.append('director')
            if person_id in [
                person.get('id') for person in row['_source'].get('actors')
            ]:
                roles.append('actor')
            if person_id in [
                person.get('id') for person in row['_source'].get('writers')
            ]:
                roles.append('writer')

            if len(roles) == 0:
                continue
            abstract_list.append(
                {'uuid': row['_source'].get('id'), 'roles': roles}
            )
        return abstract_list


@lru_cache()
def get_person_service(
    elastic: AsyncElasticsearch = Depends(get_elastic)
) -> PersonService:
    search_engine = ElasticAsyncSearchEngine(elastic=elastic)
    return PersonService(search_engine=search_engine)
