from dataclasses import dataclass


class Event:
    pass


@dataclass
class UrlEncoded(Event):
    code: str


@dataclass
class ShortUrlDecoded(Event):
    url: str
