FROM python:3.13.0-alpine3.20

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /app/

RUN python -m venv /py

RUN /py/bin/pip install --upgrade pip

# Install postgresql-client
RUN apk update && apk add --no-cache postgresql-client

# Install build-base and postgresql-dev
RUN apk add --no-cache --virtual .tmp build-base

RUN apk add --no-cache postgresql-dev
RUN pip install -r requirements.txt

COPY ./core /app/

