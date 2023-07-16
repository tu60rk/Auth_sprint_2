from http import HTTPStatus
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_cache.decorator import cache
from typing_extensions import Annotated
from typing import List

from api.v1.common import PaginateQueryParams
from api.v1.models import ShortFilm, Person
from core.config import settings
from services.person import PersonService, get_person_service


router = APIRouter()


@router.get("/{person_id}/film/",
            response_model=List[ShortFilm],
            summary="Поиск кинопроизведений по персоне",
            description="Поиск кинопроизведений по id персоне",
            response_description="Название и рейтинг фильма",
            tags=['Персона']
            )
@cache(expire=settings.redis_cache_expires)
async def films_by_person_id(
    person_id: uuid.UUID,
    pages: Annotated[PaginateQueryParams, Depends()],
    person_service: PersonService = Depends(get_person_service),
) -> List[ShortFilm]:
    films = await person_service.get_films_by_person_id(
        person_id=person_id,
        page_size=pages.page_size,
        page_number=pages.page_number,
    )

    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="films not found"
        )
    return [
        ShortFilm(
            id=row.id,
            title=row.title,
            imdb_raiting=row.imdb_raiting
        ) for row in films]


@router.get("/{person_id}/",
            response_model=Person,
            summary="Данные о персоне",
            description="Поиск персоны и фильмов, связанных с ним",
            response_description="ФИО персоны и роли в фильмах",
            tags=['Персона']
            )
@cache(expire=settings.redis_cache_expires)
async def person_by_id(
    person_id: uuid.UUID,
    person_service: PersonService = Depends(get_person_service),
) -> Person:
    person = await person_service.get_by_id(
        person_id=person_id,
    )

    if not person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="person not found"
        )
    return Person(
        uuid=person.uuid,
        full_name=person.full_name,
        films=person.films
    )


@router.get("/search",
            response_model=List[Person],
            summary="Поиск персон",
            description="Поиск персоны и фильмов",
            response_description="ФИО персоны ",
            tags=['Поиск']
            )
@cache(expire=settings.redis_cache_expires)
async def person_search(
    pages: Annotated[PaginateQueryParams, Depends()],
    person_service: PersonService = Depends(get_person_service),
    query: str = Query(
        title="Search by text.",
        description="Searching by text query"
    ),
) -> List[Person]:
    persons = await person_service.get_by_search(
        query=query,
        page_size=pages.page_size,
        page_number=pages.page_number,
    )

    if not persons:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="person not found"
        )
    return [
            Person(
                uuid=row.uuid,
                full_name=row.full_name,
                films=row.films
            ) for row in persons
        ]
