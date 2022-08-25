FROM jopplt/python-poetry:3.10 AS base
RUN apk add --no-cache \
    gcc \
    libc-dev \
    linux-headers \
    pcre-dev
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-dev
COPY app .
EXPOSE 5000
CMD [ "uwsgi", "--ini", "app.ini" ]
