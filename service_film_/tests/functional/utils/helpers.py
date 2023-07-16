import aiohttp
import elasticsearch
import functools
import redis
import logging
import time

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10):
    """
    Функция для повторного выполнения функции через некоторое время, если возникла ошибка. Использует наивный экспоненциальный рост времени повтора (factor) до граничного времени ожидания (border_sleep_time)

    Формула:
        t = start_sleep_time * 2^(n) if t < border_sleep_time
        t = border_sleep_time if t >= border_sleep_time
    :param start_sleep_time: начальное время повтора
    :param factor: во сколько раз нужно увеличить время ожидания
    :param border_sleep_time: граничное время ожидания
    :return: результат выполнения функции
    """

    def func_wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            secsleep = start_sleep_time
            while True:
                try:
                    return func(*args, **kwargs)
                except (
                    elasticsearch.ConnectionError,
                    elasticsearch.ConnectionTimeout,
                    elasticsearch.AuthenticationException,
                    elasticsearch.AuthorizationException,
                    redis.exceptions.MaxConnectionsError,
                    redis.exceptions.ConnectionError,
                    aiohttp.client_exceptions.ClientConnectorError
                ) as err:
                    logger.error(f"""** Could not connect to Elastic/Redis.
Wait {secsleep} seconds and repeat connection to Elastic/Redis **""")
                    logger.error(err)
                    time.sleep(secsleep)
                    if secsleep < border_sleep_time:
                        secsleep = secsleep * 2 ** (factor)
                    if secsleep >= border_sleep_time:
                        secsleep = border_sleep_time

        return inner

    return func_wrapper
