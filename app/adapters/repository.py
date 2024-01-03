from application.model import ShortUrlEntity
from application.ports.repository import ShortUrlRepository
from redis import Redis


class RedisShortUrlRepository(ShortUrlRepository):
    HASH_NAME = "short_urls"

    def __init__(self, client: Redis):
        self.client = client

    def add(self, entity: ShortUrlEntity) -> None:
        self.client.hset(
            name=self.HASH_NAME, key=str(entity.code), value=str(entity.original_url)
        )

    def get(self, key: str) -> ShortUrlEntity | None:
        value = self.client.hget(name=self.HASH_NAME, key=key)

        if not value:
            return None

        return ShortUrlEntity(original_url=value)
