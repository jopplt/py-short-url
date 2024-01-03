from dataclasses import dataclass


@dataclass
class CodeIsNotAvailable(RuntimeError):
    code: str


@dataclass
class UrlNotFound(RuntimeError):
    code: str
