#!/bin/bash

gunicorn --workers 1 --worker-class uvicorn.workers.UvicornWorker src.main:app --bind $UGC_APP_HOST:$UGC_APP_PORT
