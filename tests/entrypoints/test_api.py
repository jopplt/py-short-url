import json
from unittest import mock

import pytest
from application import errors
from application.app import App
from domain import commands, events


@pytest.mark.parametrize(
    "data, headers, command, event, exception, expected_status_code",
    [
        (
            {"url": "https://test.io"},
            {"content-type": "application/json"},
            commands.Encode(url="https://test.io"),
            events.UrlEncoded(code="test"),
            None,
            200,
        ),
        (
            "invalid_json",
            {},
            None,
            None,
            None,
            400,
        ),
        (
            {"wrong_key": "https://test.io"},
            {"content-type": "application/json"},
            None,
            None,
            None,
            400,
        ),
        (
            {"url": "invalid_url"},
            {"content-type": "application/json"},
            None,
            None,
            None,
            400,
        ),
        (
            {"url": "https://test.io"},
            {"content-type": "application/json"},
            commands.Encode(url="https://test.io"),
            events.UrlEncoded(code="test"),
            errors.HandlerError("Test error"),
            500,
        ),
        (
            {"url": "https://test.io"},
            {"content-type": "application/json"},
            commands.Encode(url="https://test.io"),
            None,
            None,
            500,
        ),
    ],
    ids=[
        "assert 200 response for valid request",
        "assert 400 response for invalid request - invalid json",
        "assert 400 response for invalid request - missing url key in body",
        "assert 400 response for invalid request - URL is not valid",
        "assert 500 response if handler raises an exception",
        "assert 500 response if handler does not return a valid event",
    ],
)
def test_encode_response(
    client, data, headers, command, event, exception, expected_status_code
):
    with mock.patch.object(
        App, "handle", return_value=event, side_effect=exception
    ) as mock_handle:
        response = client.put(
            "encode",
            data=json.dumps(data),
            headers=headers,
        )
        if command:
            mock_handle.assert_called_with(command)
        else:
            mock_handle.assert_not_called()
        assert response.status_code == expected_status_code


@pytest.mark.parametrize(
    "code, command, event, exception, expected_status_code",
    [
        (
            "test",
            commands.Decode(code="test"),
            events.ShortUrlDecoded(url="https://test.io"),
            None,
            200,
        ),
        (
            "missing",
            commands.Decode(code="missing"),
            events.UrlNotFound(),
            None,
            404,
        ),
        (
            "test",
            commands.Decode(code="test"),
            None,
            errors.HandlerError("Test error"),
            500,
        ),
        (
            "test",
            commands.Decode(code="test"),
            None,
            None,
            500,
        ),
    ],
    ids=[
        "assert 200 response for valid request",
        "assert 404 response for non existing short code",
        "assert 500 response if handler raises an exception",
        "assert 500 response if handler does not return a valid event",
    ],
)
def test_decode_response(client, code, command, event, exception, expected_status_code):
    with mock.patch.object(
        App, "handle", return_value=event, side_effect=exception
    ) as mock_handle:
        response = client.get(f"decode/{code}")
        mock_handle.assert_called_with(command)
        assert response.status_code == expected_status_code
