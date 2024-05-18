FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /frcmapp

COPY ./pyproject.toml ./cert.pem ./key.pem /frcmapp/

RUN pip install poetry
RUN poetry config virtualenvs.create true
RUN poetry install --only main

COPY ./src ./tests /frcmapp/