FROM python:3.10


ENV HOME_APP=/app

RUN addgroup --system app && adduser --system --group app
RUN mkdir $HOME_APP
RUN mkdir $HOME_APP/static

WORKDIR $HOME_APP

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV DJANGO_SETTINGS_MODULE 'config.settings'

COPY ./service_admin/requirements.txt requirements.txt
COPY ./service_admin/entrypoint.sh entrypoint.sh

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt

COPY ./service_admin/ $HOME_APP
COPY ./admin.env /app/config/.env

RUN chown -R app:app $HOME_APP
RUN chmod +x entrypoint.sh
# change to the app user
USER app


ENTRYPOINT ["/app/entrypoint.sh"]