FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /app/

RUN python -m venv /py

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


COPY ./core /app/
