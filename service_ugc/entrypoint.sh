#!/bin/bash

gunicorn --workers 1 --worker-class uvicorn.workers.UvicornWorker src.main:app --bind 0.0.0.0:8000
