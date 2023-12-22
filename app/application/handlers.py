from typing import Generic, TypeVar

from application import repository as _repository
from domain import commands as _commands
from domain import errors as _errors
from domain import events as _events
from domain import model as _model
from domain import queries as _queries

C = TypeVar("C", bound=_commands.Command | _queries.Query)
E = TypeVar("E", bound=_events.Event)
R = TypeVar("R", bound=_repository.AbstractRepository)


class Handler(Generic[R, C, E]):
    def __init__(self, repository: R):
        self.repository = repository

    def handle(self, request: C) -> E:
        raise NotImplementedError


class EncodeHandler(
    Handler[_repository.ShortUrlRepository, _commands.Encode, _events.UrlEncoded]
):
    def handle(self, request: _commands.Encode) -> _events.UrlEncoded:

        encoded = _model.ShortUrlEntity(original_url=request.url)
        found = self.repository.get(key=encoded.code)

        if not found:
            self.repository.add(encoded)
            return _events.UrlEncoded(code=encoded.code)

        if found.original_url != request.url:
            raise _errors.CodeIsNotAvailable(code=found.code)

        return _events.UrlEncoded(code=found.code)


class DecodeHandler(
    Handler[
        _repository.ShortUrlRepository,
        _queries.Decode,
        _events.ShortUrlDecoded,
    ]
):
    def handle(self, request: _queries.Decode) -> _events.ShortUrlDecoded:
        if found := self.repository.get(key=request.code):
            return _events.ShortUrlDecoded(url=found.original_url)

        raise _errors.UrlNotFound(code=request.code)
