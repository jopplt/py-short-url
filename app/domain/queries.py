from dataclasses import dataclass


class Query:
    pass


@dataclass
class Decode(Query):
    code: str
