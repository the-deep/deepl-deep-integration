# syntax=docker/dockerfile:1.2

FROM python:3.8-slim-buster

LABEL maintainer="Deep Dev dev@thedeep.com"

WORKDIR /code

RUN apt-get update \
    && apt-get -y install git gcc curl openssh-client

RUN pip install --upgrade pip setuptools wheel

COPY mockserver/requirements.txt /code
RUN pip install -r requirements.txt

RUN mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts

RUN echo "$SSH_PRV_KEY" > /root/.ssh/id_rsa && \
    chmod 700 /root/.ssh/id_rsa

RUN --mount=type=ssh \
    pip install git+ssh://git@github.com/the-deep/deepl-pdf-extraction.git

COPY . /code/

EXPOSE 8001
