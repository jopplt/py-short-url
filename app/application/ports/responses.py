import dataclasses as _dc


@_dc.dataclass
class Response:
    pass


@_dc.dataclass
class EncodedUrl(Response):
    code: str


@_dc.dataclass
class DecodedUrl(Response):
    url: str
