import logging
from typing import Dict, Type

from . import handlers as _handlers
from .ports import repository as _repository
from .ports import requests as _requests
from .ports import responses as _responses


class App:
    def __init__(
        self,
        repository: _repository.ShortUrlRepository,
        logger: logging.Logger,
    ):
        self.repository = repository
        self.logger = logger

        self.handlers: Dict[Type[_requests.Request], _handlers.Handler] = {
            _requests.EncodeUrl: _handlers.EncodeHandler(repository=self.repository),
            _requests.DecodeShortenedUrl: _handlers.DecodeHandler(
                repository=self.repository
            ),
        }

    def handle(self, request: _requests.Request) -> _responses.Response:
        if not type(request) in self.handlers:
            raise NotImplementedError(f"Missing handler for {type(request)}")

        return self.handlers[type(request)].handle(request)
