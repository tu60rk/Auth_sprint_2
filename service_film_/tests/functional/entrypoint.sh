#!/bin/sh

while ! curl $ELASTIC_HOST:$ELASTIC_PORT; do
    sleep 10
done

sleep 5
curl -XPUT http://$ELASTIC_HOST:$ELASTIC_PORT/movies -H 'Content-Type: application/json' -d @/tests/functional/index_movies.json
sleep 5
curl -XPUT http://$ELASTIC_HOST:$ELASTIC_PORT/genres -H 'Content-Type: application/json' -d @/tests/functional/index_genres.json
sleep 5
curl -XPUT http://$ELASTIC_HOST:$ELASTIC_PORT/persons -H 'Content-Type: application/json' -d @/tests/functional/index_persons.json
sleep 5

python /tests/functional/utils/wait_for_redis.py
pytest /tests/functional/src

exec "$@"