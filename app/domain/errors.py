from dataclasses import dataclass


@dataclass
class DomainError(RuntimeError):
    pass


@dataclass
class CodeIsNotAvailable(DomainError):
    code: str


@dataclass
class UrlNotFound(DomainError):
    code: str
