import uuid
from pydantic import BaseModel
from datetime import datetime


class FilmProgress(BaseModel):
    movie_id: uuid.UUID
    user_id: uuid.UUID
    description: str
    event_date: datetime
