FROM python:3.8-alpine
MAINTAINER zube.dev

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /Recipe_API_Project
WORKDIR /Recipe_API_Project
COPY . /Recipe_API_Project

RUN mkdir -p /web/media
RUN mkdir -p /web/static
RUN addgroup -g 994 jenkins
RUN adduser -D -u 997 -g jenkins -G jenkins
RUN chown -R jenkins:jenkins /web/
RUN chmod -R 755 /web
USER jenkins