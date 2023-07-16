FROM python:3.10-slim-buster

ENV PYTHONPATH=./
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


COPY ./elastic/index_genres.json /tests/functional/index_genres.json
COPY ./elastic/index_persons.json /tests/functional/index_persons.json
COPY ./elastic/index_movies.json /tests/functional/index_movies.json
COPY ./tests/functional/ /tests/functional/


RUN apt-get -qq update
RUN apt-get -y install curl
RUN pip install --no-cache-dir -r /tests/functional/requirements.txt
RUN chmod +x /tests/functional/entrypoint.sh

CMD ["/tests/functional/entrypoint.sh"]