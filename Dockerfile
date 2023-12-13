FROM jopplt/python:3.11-poetry1.2.2 AS base
RUN apk add --no-cache \
    gcc \
    libc-dev \
    linux-headers \
    pcre-dev \
    libffi-dev
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-dev
COPY app .
EXPOSE 5000
CMD [ "uwsgi", "--ini", "app.ini" ]
