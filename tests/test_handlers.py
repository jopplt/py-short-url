from contextlib import nullcontext
from dataclasses import dataclass
from typing import Any
from unittest import mock

import pytest
from application import handlers
from domain import commands, events, model, queries


@dataclass
class MethodMock:
    function: str
    return_value: Any
    side_effect: Any


@pytest.mark.parametrize(
    "command, mocks, expected, expected_context",
    [
        (
            commands.Encode(url="https://test.io"),
            [
                MethodMock(
                    function="get",
                    return_value=None,
                    side_effect=None,
                )
            ],
            events.UrlEncoded(code="igokzx"),
            nullcontext(),
        ),
        (
            commands.Encode(url="https://test.io"),
            [
                MethodMock(
                    function="get",
                    return_value=model.ShortUrlEntity(
                        original_url="https://test.io",
                        code="igokzx",
                    ),
                    side_effect=None,
                )
            ],
            events.UrlEncoded(code="igokzx"),
            nullcontext(),
        ),
        (
            commands.Encode(url="https://test.io"),
            [
                MethodMock(
                    function="get",
                    return_value=model.ShortUrlEntity(
                        original_url="https://another.test.io",
                        code="igokzx",
                    ),
                    side_effect=None,
                )
            ],
            None,
            pytest.raises(RuntimeError),
        ),
    ],
    ids=[
        "encode new url",
        "encode existing url",
        "encode produces an existing short code",
    ],
)
def test_encode_handler(command, mocks, expected, expected_context):
    with mock.patch("application.repository.ShortUrlRepository") as mock_repository:
        for method_mock in mocks:
            getattr(
                mock_repository(), method_mock.function
            ).return_value = method_mock.return_value
            getattr(
                mock_repository(), method_mock.function
            ).side_effect = method_mock.side_effect

        with expected_context:
            handler = handlers.EncodeHandler(repository=mock_repository())
            actual = handler.handle(request=command)
            assert actual == expected


@pytest.mark.parametrize(
    "query, mocks, expected, expected_context",
    [
        (
            queries.Decode(code="igokzx"),
            [
                MethodMock(
                    function="get",
                    return_value=model.ShortUrlEntity(
                        original_url="https://test.io",
                        code="igokzx",
                    ),
                    side_effect=None,
                )
            ],
            events.ShortUrlDecoded(url="https://test.io"),
            nullcontext(),
        ),
        (
            queries.Decode(code="igokzx"),
            [
                MethodMock(
                    function="get",
                    return_value=None,
                    side_effect=None,
                )
            ],
            events.UrlNotFound(),
            nullcontext(),
        ),
    ],
    ids=[
        "decode stored code",
        "decode unknown code",
    ],
)
def test_decode_handler(query, mocks, expected, expected_context):
    with mock.patch("application.repository.ShortUrlRepository") as mock_repository:
        for method_mock in mocks:
            getattr(
                mock_repository(), method_mock.function
            ).return_value = method_mock.return_value
            getattr(
                mock_repository(), method_mock.function
            ).side_effect = method_mock.side_effect

        with expected_context:
            handler = handlers.DecodeHandler(repository=mock_repository())
            actual = handler.handle(request=query)
            assert actual == expected


def test_generic_handler():
    with mock.patch("application.repository.AbstractRepository") as mock_repository:
        handler = handlers.Handler(repository=mock_repository)

        with pytest.raises(NotImplementedError):
            handler.handle(request=commands.Command())
