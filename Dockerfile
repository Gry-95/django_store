FROM python:3.9-alpine3.16

COPY requirements.txt /temp/requirments.txt
COPY django_store /store
WORKDIR /store
EXPOSE 8000

RUN apk add postgresql-client build-base postgresql-dev

RUN pip install -r /temp/requirments.txt

RUN adduser --disabled-password store-user

USER store-user