# URL Shortener

![coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/jopplt/43de0052ef7377c883bb8f7547f3d767/raw/pytest-coverage-comment__main.json)


## Installation

```bash
poetry install
```

## Usage

Start redis server:
```bash
docker run -d --rm --name redis -p 6379:6379 redis:7.0-alpine redis-server --save 60 1
```

Start application:
```bash
poetry run python app/wsgi.py -p 5005
```

Use the application to create a short url:
```bash
curl -X PUT 0.0.0.0:5005/encode --header "Content-Type: application/json" --data '{"url":"https://google.com"}'
```

Try to decode the short url:
```bash
curl -X GET 0.0.0.0:5005/decode/bqrvjs
```

## Tests

```bash
poetry run pytest
```