FROM jopplt/python-poetry:3.10 AS base
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-dev
COPY app .
EXPOSE 5000
CMD [ "uwsgi", "--ini", "app.ini" ]
