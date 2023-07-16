from redis.client import Redis

from tests.functional.settings import test_settings as sett
from tests.functional.utils.helpers import backoff


@backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10)
def main():
    redis_client = Redis(host=sett.redis_host, port=sett.redis_port)
    redis_client.ping()


if __name__ == '__main__':
    main()
