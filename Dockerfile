# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

FROM python:3.11-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy dependencies and stuff
COPY src/* src/
COPY ./pyproject.toml ./poetry.lock /app/

# Installing poetry and dependencies
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --only main

# Copy the source code into the container.
COPY . /app/

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
# ENTRYPOINT [ "poetry", "run"]

CMD poetry run uvicorn src.main:app 