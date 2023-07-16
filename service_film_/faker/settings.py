import os

# Настройки Elasticsearch
ELASTIC_HOST = os.getenv("FILM_ELASTIC_HOST", "127.0.0.1")
ELASTIC_PORT = int(os.getenv("FILM_ELASTIC_PORT", 9200))
ELASTIC_SCHEME = os.getenv("FILM_ELASTIC_SCHEME", "http")
