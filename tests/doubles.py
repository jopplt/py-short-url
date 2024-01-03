from adapters import repository
from application import model


class SpyShortUrlRepository(repository.RedisShortUrlRepository):
    def __init__(self, client):
        self.calls = {"add": [], "get": []}
        super().__init__(client)

    def add(self, entity: model.ShortUrlEntity) -> None:
        self.calls["add"].append({"entity": entity})
        return super().add(entity)

    def get(self, key: str) -> model.ShortUrlEntity | None:
        self.calls["get"].append({"key": key})
        return super().get(key)
