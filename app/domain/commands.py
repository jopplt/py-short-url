from dataclasses import dataclass


class Command:
    pass


@dataclass
class Encode(Command):
    url: str
