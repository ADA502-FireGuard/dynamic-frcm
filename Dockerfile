FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /frcmapp

COPY ./pyproject.toml ./cert.pem ./key.pem /frcmapp/

RUN pip install poetry
RUN poetry config virtualenvs.create true
RUN poetry install --no-dev

COPY ./src /frcmapp/

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--ssl-keyfile", "key.pem", "--ssl-certfile", "cert.pem"]