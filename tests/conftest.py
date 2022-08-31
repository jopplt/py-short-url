import logging

import pytest
from adapters import repository
from application import handlers, main
from domain import commands
from entrypoints.api import ApiFactory


@pytest.fixture()
def api_factory():
    yield ApiFactory()


@pytest.fixture()
def redis_fake_client():
    import fakeredis

    return fakeredis.FakeStrictRedis(version=7, decode_responses=True)


@pytest.fixture()
def fake_short_url_repository(redis_fake_client):
    return repository.RedisShortUrlRepository(client=redis_fake_client)


@pytest.fixture()
def fake_logger():
    return logging.getLogger("test")


@pytest.fixture()
def fake_app(fake_short_url_repository, fake_logger):
    return main.App(
        handlers={
            commands.Encode: handlers.EncodeHandler(
                repository=fake_short_url_repository
            ),
            commands.Decode: handlers.DecodeHandler(
                repository=fake_short_url_repository
            ),
        },
        logger=fake_logger,
    )


@pytest.fixture()
def fake_api(api_factory, fake_app):
    yield api_factory.create(application=fake_app)


@pytest.fixture()
def fake_client(fake_api):
    return fake_api.test_client()
