FROM python:3.8.7-alpine

ARG BUILD_PACKAGES="bash curl make gcc libc-dev postgresql-dev"

RUN apk add --update \
    $BUILD_PACKAGES \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py \
    | python 

ENV PATH="${PATH}:/root/.poetry/bin"
WORKDIR /app/
COPY . /app

RUN poetry config virtualenvs.create false && poetry install --no-interaction
