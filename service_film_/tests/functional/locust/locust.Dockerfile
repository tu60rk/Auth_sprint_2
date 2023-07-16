FROM python:3.10-slim-buster

ENV PYTHONPATH=./
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /locust/requirements.txt
COPY ./locust/locust_tests.py /locust/locust_tests.py

RUN pip install --no-cache-dir -r /locust/requirements.txt

# CMD ["locust", "-f", "/locust/locust_tests.py", "--host=http://service:${APP_PORT}"]