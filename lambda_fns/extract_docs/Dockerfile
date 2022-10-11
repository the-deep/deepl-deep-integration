# syntax=docker/dockerfile:1.2

FROM python:3.10-slim-buster

LABEL maintainer="Deep Dev dev@thedeep.com"

WORKDIR /code

COPY pyproject.toml poetry.lock /code/

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
        # Build required packages
        git gcc curl \
    # Upgrade pip and install python packages for code
    && cd /code/ \
    && pip install --upgrade --no-cache-dir pip poetry \
    && poetry --version \
    # Configure to use system instead of virtualenvs
    && poetry config virtualenvs.create false \
    && poetry install --no-root \
    # Clean-up
    && pip uninstall -y poetry virtualenv-clone virtualenv \
    && apt-get remove -y gcc \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

COPY deepex_ecs/app.py content_types.py wget.py s3_handler.py config.py /code/
