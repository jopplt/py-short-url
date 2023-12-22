import logging
import os

import redis
from adapters.repository import RedisShortUrlRepository
from application import handlers, main
from domain import commands, queries

_redis = redis.StrictRedis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    password=os.getenv("REDIS_PASSWORD", None),
    decode_responses=True,
)

_short_url_repository = RedisShortUrlRepository(client=_redis)

_logger = logging.getLogger("werkzeug")

app = main.App(
    handlers={
        commands.Encode: handlers.EncodeHandler(repository=_short_url_repository),
        queries.Decode: handlers.DecodeHandler(repository=_short_url_repository),
    },
    logger=_logger,
)
