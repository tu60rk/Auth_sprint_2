import orjson
import uuid
from pydantic import BaseModel
from typing import List, Optional


def orjson_dumps(v, *, default):
    # orjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декодируем
    return orjson.dumps(v, default=default).decode()


class OrjsonMixin:
    class Config:
        # Заменяем стандартную работу с json на более быструю
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Common(BaseModel):
    id: uuid.UUID
    name: str


class Genres(BaseModel, OrjsonMixin):
    id: uuid.UUID
    name: str
    description: Optional[str] = None


class Film(BaseModel, OrjsonMixin):
    id: uuid.UUID
    title: str
    description: str
    imdb_raiting: Optional[float] = 0.0
    genres: Optional[List[Genres]] = None
    actors: Optional[List[Common]] = None
    writers: Optional[List[Common]] = None
    directors: Optional[List[Common]] = None


class Films(BaseModel, OrjsonMixin):
    id: uuid.UUID
    title: str
    imdb_raiting: Optional[float] = 0.0
