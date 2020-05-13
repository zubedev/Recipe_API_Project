FROM python:3.8-alpine
MAINTAINER zube.dev

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /Recipe_API_Project
WORKDIR /Recipe_API_Project
COPY . /Recipe_API_Project

RUN adduser -D user
USER user