FROM python:3.10


ENV HOME_APP=/app

RUN addgroup --system app && adduser --system --group app
RUN mkdir $HOME_APP
RUN mkdir $HOME_APP/static

WORKDIR $HOME_APP

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV DJANGO_SETTINGS_MODULE 'config.settings'

COPY requirements.txt requirements.txt
COPY entrypoint.sh entrypoint.sh

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt

COPY . $HOME_APP

RUN chown -R app:app $HOME_APP
RUN chmod +x entrypoint.sh
# change to the app user
USER app


ENTRYPOINT ["/app/entrypoint.sh"]