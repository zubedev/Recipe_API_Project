FROM python:3.8-alpine
MAINTAINER zube.dev

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /Recipe_API_Project
WORKDIR /Recipe_API_Project
COPY . /Recipe_API_Project

RUN adduser -D user
USER user