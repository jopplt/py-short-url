from typing import Generic, TypeVar, Union

from application import repository as _repository
from domain import commands as _commands
from domain import events as _events
from domain import model as _model

C = TypeVar("C", bound=_commands.Command)
E = TypeVar("E", bound=_events.Event)
R = TypeVar("R", bound=_repository.AbstractRepository)


class Handler(Generic[R, C, E]):
    def __init__(self, repository: R):
        self.repository = repository

    def handle(self, command: C) -> E:
        raise NotImplementedError


class EncodeHandler(
    Handler[_repository.ShortUrlRepository, _commands.Encode, _events.UrlEncoded]
):
    def handle(self, command: _commands.Encode) -> _events.UrlEncoded:

        code = self._generate_short_code(url=command.url)
        found = self.repository.get(key=code)

        if not found:
            self.repository.add(
                _model.ShortUrlEntity(
                    original_url=command.url,
                    code=code,
                )
            )
            return _events.UrlEncoded(code=code)

        if found.original_url != command.url:
            raise RuntimeError("Generated code is already used by another url")

        return _events.UrlEncoded(code=found.code)

    @staticmethod
    def _generate_short_code(url: str) -> str:
        import base64
        import hashlib
        import re

        return re.sub(
            r"[^\w\d]",
            "",
            base64.urlsafe_b64encode(
                hashlib.sha256(f"{url}".encode()).digest()
            ).decode(),
        )[:6].lower()


class DecodeHandler(
    Handler[
        _repository.ShortUrlRepository,
        _commands.Decode,
        Union[_events.UrlNotFound, _events.ShortUrlDecoded],
    ]
):
    def handle(
        self, command: _commands.Decode
    ) -> Union[_events.UrlNotFound, _events.ShortUrlDecoded]:
        if found := self.repository.get(key=command.code):
            return _events.ShortUrlDecoded(url=found.original_url)

        return _events.UrlNotFound()
