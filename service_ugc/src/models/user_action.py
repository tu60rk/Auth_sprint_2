from pydantic import BaseModel
from datetime import datetime

class FilmProgress(BaseModel):
    movie_id: str
    user_id: str
    description: str  # "Просмотрел Иронию судьбы с 00:53:24 до 00:53:25 (1 секунду)"
    event_date: datetime