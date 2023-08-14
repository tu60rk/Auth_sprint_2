from fastapi import APIRouter
from src.services.user_action import record_progress
from service_ugc.src.models.user_action import FilmProgress

router = APIRouter()

film_progress_db = {}

@router.post("")
async def record_film_progress(progress: FilmProgress):
    record_progress(progress)
    return {
        "message": f"Film progress recorded successfully for movie_id {progress.movie_id} and user_id {progress.user_id}."}

# @router.post("/producer/film_progress")
# async def record_film_progress(progress: FilmProgress):
#     key = (progress.user_id, progress.movie_id)
#     film_progress_db[key] = progress
#     return {
#         "message": f"Film progress recorded successfully for movie_id {progress.movie_id} and user_id {progress.user_id}."}
