from typing import Union

from application.repository import AbstractRepository, ShortUrlRepository
from domain import commands, events


class Handler:
    def __init__(self, repository: AbstractRepository):
        self.repository = repository

    def handle(self, command: commands.Command) -> events.Event:
        raise NotImplementedError


class EncodeHandler(Handler):
    def __init__(self, repository: ShortUrlRepository):
        super().__init__(repository=repository)

    def handle(self, command: commands.Encode) -> events.UrlEncoded:
        from domain.model import ShortUrlEntity

        code = self._generate_short_code(url=command.url)
        found = self.repository.get(key=code)

        if not found:
            self.repository.add(
                ShortUrlEntity(
                    original_url=command.url,
                    code=code,
                )
            )
            return events.UrlEncoded(code=code)

        if found.original_url != command.url:
            raise RuntimeError("Generated code is already used by another url")

        return events.UrlEncoded(code=found.code)

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


class DecodeHandler(Handler):
    def __init__(self, repository: ShortUrlRepository):
        super().__init__(repository=repository)

    def handle(
        self, command: commands.Decode
    ) -> Union[events.UrlNotFound, events.ShortUrlDecoded]:
        if found := self.repository.get(key=command.code):
            return events.ShortUrlDecoded(url=found.original_url)

        return events.UrlNotFound()
