from http import HTTPStatus
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_cache.decorator import cache
from typing_extensions import Annotated
from typing import List

from api.v1.common import PaginateQueryParams
from api.v1.models import ShortFilm, FilmDetail
from core.config import settings
from services.film import FilmService, get_film_service


router = APIRouter()


@router.get("/search",
            response_model=List[ShortFilm],
            summary="Поиск кинопроизведений",
            description="Полнотекстовый поиск по кинопроизведениям",
            response_description="Название и рейтинг фильма",
            tags=['Поиск']
            )
@cache(expire=settings.redis_cache_expires)
async def film_search(
    pages: Annotated[PaginateQueryParams, Depends()],
    film_service: FilmService = Depends(get_film_service),
    query: str = Query(
        title="Search by text.",
        description="Searching by text query"
    ),
) -> List[ShortFilm]:
    films = await film_service.get_by_search(
        query=query,
        page_size=pages.page_size,
        page_number=pages.page_number,
    )

    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="films not found"
        )

    return [ShortFilm(
        id=row.id,
        title=row.title,
        imdb_raiting=row.imdb_raiting
    ) for row in films]


@router.get(
    "",
    response_model=List[ShortFilm],
    summary="Список популярных фильмов",
    description="",
    response_description="Что-то",
    tags=["Кинопроизведение"],
)
@cache(expire=settings.redis_cache_expires)
async def films(
    pages: Annotated[PaginateQueryParams, Depends()],
    film_service: FilmService = Depends(get_film_service),
    genre: uuid.UUID = None,
    sort_param: str = Query(
        default='-imdb_raiting',
        title="Sort by field.",
        description="Sorting by field in films"
    ),
) -> List[ShortFilm]:
    films = await film_service.get_all(
        sort_param=sort_param,
        page_size=pages.page_size,
        page_number=pages.page_number,
        genre=genre
    )

    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="films not found"
        )

    return [ShortFilm(
        id=row.id,
        title=row.title,
        imdb_raiting=row.imdb_raiting
    ) for row in films]


@router.get(
    "/{film_id}",
    response_model=FilmDetail,
    summary="Информация по кинопроизведению",
    description="Полная информация по кинопроизведению/кинопроизведениям",
    response_description="Что-то",
    tags=["Кинопроизведение"],
)
@cache(expire=60)
async def film_details(
    film_id: uuid.UUID,
    film_service: FilmService = Depends(get_film_service)
) -> FilmDetail:

    film = await film_service.get_by_id(film_id)

    if not film:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="film not found"
        )

    return FilmDetail(
        id=film.id,
        title=film.title,
        description=film.description,
        imdb_raiting=film.imdb_raiting,
        genres=film.genres,
        actors=film.actors,
        writers=film.writers,
        directors=film.directors,
    )
