import orjson
import uuid
from pydantic import BaseModel
from typing import List, Optional


def orjson_dumps(v, *, default):
    # orjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декодируем
    return orjson.dumps(v, default=default).decode()


class Films(BaseModel):
    uuid: uuid.UUID
    roles: List[str]


class Person(BaseModel):
    uuid: uuid.UUID
    full_name: str
    films: Optional[List[Films]] = None
