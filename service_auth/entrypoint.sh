#!/bin/bash

result=$( alembic current )
if [ $result -eq 1 ]
then
    echo 'migrations applied';
else
    alembic revision --autogenerate -m "first_migration" --rev-id="1" && \
    alembic upgrade head;
fi

gunicorn --workers 1 --worker-class uvicorn.workers.UvicornWorker src.main:app --bind $AUTH_APP_HOST:$AUTH_APP_PORT