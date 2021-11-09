FROM python:3.8-slim-buster

LABEL maintainer="ToggleCorp Dev dev@togglecorp.com"

COPY . /code/
WORKDIR /code

RUN apt-get update \
    && apt-get -y install git
RUN pip install --upgrade pip setuptools wheel

RUN pip install -r mockserver/requirements.txt


EXPOSE 8001
