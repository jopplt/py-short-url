from typing import Any, Tuple

import pydantic
from application import errors
from bootstrap import app
from domain import commands, events
from flasgger import Swagger
from flask import Flask, request
from werkzeug.exceptions import BadRequest
from werkzeug.http import HTTP_STATUS_CODES

flask_app = Flask(__name__)
swagger = Swagger(
    flask_app,
    config={
        "headers": [],
        "title": "URL Shortener",
        "specs": [
            {
                "endpoint": "apispec_1",
                "route": "/apispec_1.json",
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/",
    },
)


class EncodeRequest(pydantic.BaseModel):
    url: pydantic.HttpUrl


@flask_app.route("/encode", methods=["PUT"])
def encode() -> Tuple[str, int]:
    """Encode
    Returns a short code for a given URL
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            url:
              type: string
              example: https://google.com
          required:
            - url
    responses:
      200:
        description: Short code for the original URL
        schema:
          type: string
    """
    try:
        content = request.get_json()
    except BadRequest as e:
        return response(e, 400)

    try:
        encode_request = EncodeRequest.parse_obj(content)
    except (pydantic.ValidationError, KeyError) as e:
        return response(e, 400)

    try:
        command = commands.Encode(url=encode_request.url)
        event = app.handle(command)
    except errors.HandlerError as e:
        return response(e, 500)

    try:
        assert isinstance(event, events.UrlEncoded)
        return response(event.code, 200)
    except AssertionError as e:
        return response(e, 500)


@flask_app.route("/decode/<code>", methods=["GET"])
def decode(code: str) -> Tuple[str, int]:
    """Decode
    Returns the original URL given a short code
    ---
    parameters:
      - in: path
        name: code
        required: true
        schema:
          type: string
          example: bqrvjs
    responses:
      200:
        description: Decoded URL
        schema:
          type: string
      404:
        description: Not found - URL was not encoded
    """
    try:
        command = commands.Decode(code=code)
        event = app.handle(command)
    except errors.HandlerError as e:
        return response(e, 500)

    if isinstance(event, events.ShortUrlDecoded):
        return response(event.url, 200)

    if isinstance(event, events.UrlNotFound):
        return response(None, 404)

    return response(None, 500)


def response(content: Any, status_code: int) -> Tuple[str, int]:
    if status_code != 200:
        if content:
            content = f"{HTTP_STATUS_CODES[status_code]}: {content}"
        else:
            content = f"{HTTP_STATUS_CODES[status_code]}"
    return content, status_code
