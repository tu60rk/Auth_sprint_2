import pandas as pd

from typing import Union, Generator
from elasticsearch import Elasticsearch, helpers


class LaodDataToEs:
    def __init__(self, es_conn: Elasticsearch) -> None:
        self.es_conn = es_conn

    def insert_data(self, index: str, data: Union[pd.DataFrame, list, dict]):

        if isinstance(data, pd.DataFrame):
            data_for_es = self.prepared_data_from_dataframe

        helpers.bulk(
            client=self.es_conn, actions=data_for_es(index=index, df=data), index=index
        )

    @staticmethod
    def get_source(row_data, type: str) -> dict:

        if type == 'movies':
            return {
                    "id": row_data["id"],
                    "imdb_raiting": row_data["raiting"],
                    "genres": list(row_data["genres"]),
                    "genre": list(["genre"]),
                    "title": row_data["title"],
                    "description": row_data["description"],
                    "directors": list(row_data["directors"]),
                    "director": list(row_data["director"]),
                    "actors_names": list(row_data["actors_names"]),
                    "actors": list(row_data["actors"]),
                    "writers_names": list(row_data["writers_names"]),
                    "writers": list(row_data["writers"]),
                }
        if type == 'genres':
            return {
                    "id": row_data["id"],
                    "name": row_data["name"],
                    "description": row_data["description"],
                }
        if type == 'persons':
            return {
                    "id": row_data["id"],
                    "full_name": row_data["name"],
                }

    def prepared_data_from_dataframe(self, index: str, df: pd.DataFrame) -> Generator:

        for idx, row in df.iterrows():
            doc = {
                "_index": index,
                "_id": row["id"],
                "_source": self.get_source(row_data=row, type=index)
            }
            yield doc
