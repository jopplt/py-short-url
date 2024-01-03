import dataclasses as _dc


@_dc.dataclass
class Request:
    pass


@_dc.dataclass
class EncodeUrl(Request):
    url: str


@_dc.dataclass
class DecodeShortenedUrl(Request):
    code: str
