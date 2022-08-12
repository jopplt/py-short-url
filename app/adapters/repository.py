from typing import Union

from application.repository import ShortUrlRepository
from domain.model import ShortUrlEntity
from redis import Redis


class RedisShortUrlRepository(ShortUrlRepository):
    HASH_NAME = "short_urls"

    def __init__(self, client: Redis):
        self.client = client

    def add(self, entity: ShortUrlEntity) -> None:
        self.client.hset(
            name=self.HASH_NAME, key=str(entity.code), value=str(entity.original_url)
        )

    def get(self, key: str) -> Union[None, ShortUrlEntity]:
        value = self.client.hget(name=self.HASH_NAME, key=key)

        if not value:
            return None

        return ShortUrlEntity(original_url=value, code=key)
