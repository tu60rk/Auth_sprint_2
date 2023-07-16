FROM python:3.10

ENV HOME_APP=/faker
RUN mkdir $HOME_APP
WORKDIR $HOME_APP

COPY ./requirements.txt $HOME_APP/

RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

COPY ./faker/entrypoint.sh $HOME_APP/
COPY ./faker/generator.py $HOME_APP/faker/
COPY ./faker/loadtoes.py $HOME_APP/faker/
COPY ./faker/main.py $HOME_APP/faker/
COPY ./faker/settings.py $HOME_APP/faker/

RUN chmod +x entrypoint.sh

CMD ["/faker/entrypoint.sh"]