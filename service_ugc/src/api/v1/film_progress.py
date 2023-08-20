from fastapi import APIRouter, HTTPException
from http import HTTPStatus

from src.services.film_progress import record_progress
from src.models.film_progress import FilmProgress

router = APIRouter()

@router.post(
    "/{topicname}",
    response_model=bool,
    status_code=HTTPStatus.ACCEPTED,
    summary="",
    tags=["Авторизация"],
)
async def kafka_produce(msg: FilmProgress, topic: str) -> bool:
    """
    Produce a message into <topicname>
    This will produce a message into a Apache Kafka topic
    And this path operation will:
    * return bool
    """
    result = await record_progress(msg=msg, topic=topic)
    if result:
        return result

    raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Something goes wrong'
        )
