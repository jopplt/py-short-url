import logging
import os

import redis
from adapters.repository import RedisShortUrlRepository
from application import main

_redis = redis.StrictRedis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    password=os.getenv("REDIS_PASSWORD", None),
    decode_responses=True,
)

_short_url_repository = RedisShortUrlRepository(client=_redis)

_logger = logging.getLogger("werkzeug")

app = main.App(
    repository=_short_url_repository,
    logger=_logger,
)
