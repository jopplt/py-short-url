from unittest import mock

import pytest
from application import main
from application.ports import errors, requests, responses


@pytest.mark.parametrize(
    "data, headers, req, resp, exception, expected_status_code",
    [
        (
            {"url": "https://test.io"},
            {"content-type": "application/json"},
            requests.EncodeUrl(url="https://test.io/"),
            responses.EncodedUrl(code="test"),
            None,
            200,
        ),
        (
            "invalid_json",
            {},
            None,
            None,
            None,
            422,
        ),
        (
            {"wrong_key": "https://test.io"},
            {"content-type": "application/json"},
            None,
            None,
            None,
            422,
        ),
        (
            {"url": "invalid_url"},
            {"content-type": "application/json"},
            None,
            None,
            None,
            422,
        ),
        (
            {"url": "https://test.io"},
            {"content-type": "application/json"},
            requests.EncodeUrl(url="https://test.io/"),
            responses.EncodedUrl(code="test"),
            RuntimeError("Test error"),
            500,
        ),
        (
            {"url": "https://test.io"},
            {"content-type": "application/json"},
            requests.EncodeUrl(url="https://test.io/"),
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
    fake_client, data, headers, req, resp, exception, expected_status_code
):
    with mock.patch.object(
        main.App, "handle", return_value=resp, side_effect=exception
    ) as mock_handle:
        response = fake_client.put(
            "encode",
            json=data,
            headers=headers,
        )
        if req:
            mock_handle.assert_called_with(req)
        else:
            mock_handle.assert_not_called()
        assert response.status_code == expected_status_code


@pytest.mark.parametrize(
    "code, req, resp, exception, expected_status_code",
    [
        (
            "test",
            requests.DecodeShortenedUrl(code="test"),
            responses.DecodedUrl(url="https://test.io"),
            None,
            200,
        ),
        (
            "missing",
            requests.DecodeShortenedUrl(code="missing"),
            None,
            errors.UrlNotFound(code="missing"),
            404,
        ),
        (
            "test",
            requests.DecodeShortenedUrl(code="test"),
            None,
            RuntimeError("Test error"),
            500,
        ),
        (
            "test",
            requests.DecodeShortenedUrl(code="test"),
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
def test_decode_response(fake_client, code, req, resp, exception, expected_status_code):
    with mock.patch.object(
        main.App, "handle", return_value=resp, side_effect=exception
    ) as mock_handle:
        response = fake_client.get(f"decode/{code}")
        mock_handle.assert_called_with(req)
        assert response.status_code == expected_status_code
