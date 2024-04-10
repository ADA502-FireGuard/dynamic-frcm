# syntax=docker/dockerfile:1

# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

ARG PYTHON_VERSION=3.12.0
FROM python:${PYTHON_VERSION}-alpine

# ENV PYTHONPATH "${PYTHONPATH}:/src"

# RUN allows to execute arbitrary shell commands, creating a new file system layer
# Best Practice: create a dedicated user to run you application otherwise it is run a root
RUN busybox addgroup -S -g 6969 src && busybox adduser -h /app -G src -D -u 6969 src

# Installing poetry
ARG POETRY_VERSION=1.7.1

ENV POETRY_VIRTUALENVS_IN_PROJECT=True

# The following installs Poetry in the given version
# one may use something called `here-documents` to write multiple lines of shell commands
# for this a few external dependencies have to be installed (GCC etc)
RUN <<EOF sh
    apk add --no-cache \
            curl \
            gcc \
            libressl-dev \
            musl-dev \
            libffi-dev
    python3 -m pip install --upgrade pip
    python3 -m pip install --no-cache-dir poetry==${POETRY_VERSION}
EOF

# Change working directory to /app, directory is created it if does not already exist
WORKDIR /app

# copy local project files into image filesystem, format: COPY <local dir> <image dir>
# The .dockerignore file is used to control which files get copied
# Every COPY creates a new file file system layer
# I.e. the following command copies everything in the project dir that is not ignored to /app
COPY src/* src/
COPY pyproject.toml .
COPY poetry.lock .

# # change current user 
# USER tempstore:tempstore

RUN poetry install


# command to execute on container startup
# first create the generic entry command (poetry in this case, which would allow us to run Python as well)
ENTRYPOINT ["poetry", "run"]
# CMD then runs poetry with the default flags
CMD ["uvicorn", "--host", "127.0.0.1", "--port", "8000", "src.main:app"]