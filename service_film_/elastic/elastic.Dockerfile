FROM node:alpine

ENV HOME_APP=/elastic
RUN mkdir $HOME_APP

RUN apk --no-cache add curl
RUN npm install elasticdump -g elasticdump

WORKDIR $HOME_APP

COPY entrypoint.sh $HOME_APP/

COPY ./dump_genres.json $HOME_APP/
COPY ./dump_movies.json $HOME_APP/
COPY ./dump_persons.json $HOME_APP/
COPY ./index_genres.json $HOME_APP/
COPY ./index_movies.json $HOME_APP/
COPY ./index_persons.json $HOME_APP/

RUN chmod +x entrypoint.sh

CMD ["/elastic/entrypoint.sh"]