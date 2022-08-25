import logging

import pytest
from application import handlers, main
from domain import commands
from entrypoints.api import ApiFactory

from tests import doubles, utils


@pytest.fixture()
def api_factory():
    yield ApiFactory()


@pytest.fixture()
def api(api_factory):
    # flask_app.config.update(
    #     {
    #         "TESTING": True,
    #     }
    # )
    with utils.override_environ(
        REDIS_HOST="test",
        REDIS_PORT="6379",
        REDIS_PASSWORD="secret",
    ):
        from bootstrap import app

        yield api_factory.create(application=app)


@pytest.fixture()
def client(api):
    return api.test_client()


@pytest.fixture()
def fake_short_url_repository():
    return doubles.FakeShortUrlRepository()


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
