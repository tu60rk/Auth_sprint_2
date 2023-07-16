import uuid
from pydantic import BaseModel
from typing import List, Optional


class Common(BaseModel):
    id: uuid.UUID
    name: str


class ShortFilm(BaseModel):
    id: uuid.UUID
    title: str
    imdb_raiting: Optional[float] = 0.0


class Genres(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str]


class FilmDetail(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    imdb_raiting: Optional[float] = 0.0
    genres: List[Genres]
    actors: Optional[List[Common]] = None
    writers: Optional[List[Common]] = None
    directors: Optional[List[Common]] = None


class FilmRoles(BaseModel):
    uuid: uuid.UUID
    roles: List[str]


class Person(BaseModel):
    uuid: uuid.UUID
    full_name: str
    films: Optional[List[FilmRoles]] = None
    films: Optional[List[FilmRoles]] = None
