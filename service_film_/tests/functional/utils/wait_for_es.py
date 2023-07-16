import time

from elasticsearch import Elasticsearch

from tests.functional.settings import test_settings as sett
from tests.functional.utils.helpers import backoff


@backoff(start_sleep_time=1, factor=2, border_sleep_time=20)
def main():
    host = f'{sett.elastic_scheme}{sett.elastic_host}:{sett.elastic_port}'
    es_client = Elasticsearch(hosts=[host])
    es_client.ping()
    # wait when data load
    time.sleep(20)


if __name__ == '__main__':
    main()
