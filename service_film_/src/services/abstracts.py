import abc

from elasticsearch import AsyncElasticsearch, NotFoundError
from typing import Any


class AsyncSearchEngine(abc.ABC):

    @abc.abstractmethod
    async def get_by_id(self, index: str, _id: str) -> Any:
        pass

    @abc.abstractmethod
    async def search(self, index: str, query: dict) -> Any:
        pass

    @staticmethod
    @abc.abstractmethod
    def prepare_query(type: str, values: list = None) -> dict:
        pass

    @staticmethod
    @abc.abstractmethod
    def prepare_sorting(sort_param: str) -> str:
        pass


class BasicService(abc.ABC):

    @abc.abstractmethod
    async def get_by_id(self, _id: str) -> dict:
        pass
