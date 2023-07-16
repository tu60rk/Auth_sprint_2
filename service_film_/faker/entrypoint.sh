#!/bin/sh

while ! curl film_elasticsearch:$FILM_ELASTIC_PORT; do
    sleep 10
done

# need to wait when elastic create indexes.
sleep 30
python faker/main.py

exec "$@"