class Entity:
    pass


class ShortUrlEntity(Entity):
    def __init__(self, original_url: str, code: str):
        self.original_url = original_url
        self.code = code
