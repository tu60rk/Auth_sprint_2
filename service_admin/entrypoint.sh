#!/bin/bash

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $ADMIN_POSTGRES_HOST $ADMIN_POSTGRES_PORT; do
      sleep 1
    done

    echo "PostgreSQL started"
fi

exec "$@"