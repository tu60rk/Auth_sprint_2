from src.models.user_action import FilmProgress

film_progress_db = {}

def record_progress(progress: FilmProgress):
    key = (progress.user_id, progress.movie_id)
    film_progress_db[key] = progress
    return progress
