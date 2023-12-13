from unittest import mock

import pytest
from application import errors, main
from domain import commands


def test_application_raises_exception_for_missing_handler(fake_logger):
    app = main.App(handlers={}, logger=fake_logger)
    with pytest.raises(errors.HandlerNotFound):
        app.handle(request=commands.Encode(url="https://test.io"))


def test_application_raises_exception_when_handler_fails(
    fake_logger, fake_short_url_repository
):
    with mock.patch("application.handlers.EncodeHandler") as mock_handler:
        getattr(mock_handler(), "handle").side_effect = errors.HandlerError()

        app = main.App(handlers={commands.Encode: mock_handler()}, logger=fake_logger)

        with pytest.raises(errors.HandlerError):
            app.handle(request=commands.Encode(url="https://test.io"))
