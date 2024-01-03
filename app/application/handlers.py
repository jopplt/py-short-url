from typing import Generic, TypeVar

from . import model as _model
from .ports import errors as _errors
from .ports import repository as _repository
from .ports import requests as _requests
from .ports import responses as _responses

Q = TypeVar("Q", bound=_requests.Request)
P = TypeVar("P", bound=_responses.Response)
R = TypeVar("R", bound=_repository.ShortUrlRepository)


class Handler(Generic[R, Q, P]):
    def __init__(self, repository: R):
        self.repository = repository

    def handle(self, request: Q) -> P:
        raise NotImplementedError  # pragma: no cover


class EncodeHandler(
    Handler[_repository.ShortUrlRepository, _requests.EncodeUrl, _responses.EncodedUrl]
):
    def handle(self, request: _requests.EncodeUrl) -> _responses.EncodedUrl:

        encoded = _model.ShortUrlEntity(original_url=request.url)
        found = self.repository.get(key=encoded.code)

        if not found:
            self.repository.add(encoded)
            return _responses.EncodedUrl(code=encoded.code)

        if found.original_url != request.url:
            raise _errors.CodeIsNotAvailable(code=found.code)

        return _responses.EncodedUrl(code=found.code)


class DecodeHandler(
    Handler[
        _repository.ShortUrlRepository,
        _requests.DecodeShortenedUrl,
        _responses.DecodedUrl,
    ]
):
    def handle(self, request: _requests.DecodeShortenedUrl) -> _responses.DecodedUrl:
        if found := self.repository.get(key=request.code):
            return _responses.DecodedUrl(url=found.original_url)

        raise _errors.UrlNotFound(code=request.code)
