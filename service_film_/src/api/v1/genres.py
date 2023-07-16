import uuid

from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from typing import List
from typing_extensions import Annotated

from api.v1.common import PaginateQueryParams
from api.v1.models import Genres
from core.config import settings
from services.genre import GenreService, get_genre_service


router = APIRouter()


@router.get(
    "/",
    response_model=List[Genres],
    summary="Список всех жанров",
    description="Получение списка всех жанров",
    response_description="Список жанров",
    tags=["Жанры"],
)
@cache(expire=settings.redis_cache_expires)
async def get_all_genres(
    pages: Annotated[PaginateQueryParams, Depends()],
    genre_service: GenreService = Depends(get_genre_service),
) -> List[Genres]:
    genres = await genre_service.get_all(
        page_size=pages.page_size,
        page_number=pages.page_number,
    )

    if not genres:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Genres not found",
        )

    return genres


@router.get(
    "/{genre_id}",
    response_model=Genres,
    summary="Информация по жанру",
    description="Получение информации о конкретном жанре",
    response_description="Информация о жанре",
    tags=["Жанры"],
)
@cache(expire=settings.redis_cache_expires)
async def get_genre_by_id(
    genre_id: uuid.UUID,
    genre_service: GenreService = Depends(get_genre_service),
) -> Genres:
    genre = await genre_service.get_by_id(genre_id)

    if not genre:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Genre not found",
        )

    return genre
