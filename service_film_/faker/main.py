import settings

from elasticsearch import Elasticsearch

from loadtoes import LaodDataToEs
from generator import GeneratorMovies


if __name__ == '__main__':
    dsl_es = {
        "host": settings.ELASTIC_HOST,
        "port": int(settings.ELASTIC_PORT),
        "scheme": settings.ELASTIC_SCHEME,
    }

    with Elasticsearch([dsl_es]) as es_conn:
        loadines = LaodDataToEs(es_conn=es_conn)
        generator = GeneratorMovies()

        # generate and load genres
        df_genres = generator.generate(type='genres', count=100)
        loadines.insert_data(index='genres', data=df_genres)

        # generate and load persons
        df_persons = generator.generate(type='persons', count=800_000)
        loadines.insert_data(index='persons', data=df_persons)

        # generate and load films
        df_films = generator.generate(type='movies', count=200_000)
        loadines.insert_data(index='movies', data=df_films)
