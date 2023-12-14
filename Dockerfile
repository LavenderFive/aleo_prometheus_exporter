# The base image we want to inherit from
FROM python:3.11.4-buster AS app

# set work directory
WORKDIR /app

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    # pip:
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry:
    POETRY_VERSION=1.5.0 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_HOME="/opt/poetry"

# System deps:
RUN pip install "poetry==$POETRY_VERSION" && poetry --version

COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-root --no-dev

ENV PYTHONUNBUFFERED="True" \
    PYTHONPATH="."

COPY . .

WORKDIR /app/src

ARG HTTP_PORT
ENV HTTP_PORT=${HTTP_PORT}
EXPOSE ${HTTP_PORT}

CMD ["python3", "main.py"]
