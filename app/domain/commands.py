from dataclasses import dataclass


class Command:
    pass


@dataclass
class Encode(Command):
    url: str


@dataclass
class Decode(Command):
    code: str
