import pytest
from application import model
from application.ports import errors, requests, responses


def test_encode_and_decode_url(fake_app):
    # Given
    # Initial State (empty repository)

    # When
    response = fake_app.handle(requests.EncodeUrl(url="https://test.io"))

    # Then
    assert fake_app.handle(
        requests.DecodeShortenedUrl(code=response.code)
    ) == responses.DecodedUrl(url="https://test.io")
    assert len(fake_app.repository.calls["add"]) == 1
    assert len(fake_app.repository.calls["get"]) == 2


def test_encode_is_idempotent(fake_app):
    # Given
    # Initial State (empty repository)

    # When
    for _ in range(3):
        fake_app.handle(requests.EncodeUrl(url="https://test.io"))

    # Then
    assert len(fake_app.repository.calls["add"]) == 1
    assert len(fake_app.repository.calls["get"]) == 3


def test_encode_with_collision_should_raise(fake_app):
    # Given
    short_url = model.ShortUrlEntity(original_url="https://test.io")
    short_url.original_url = "https://test.io/foo/"  # generate a collision
    fake_app.repository.add(entity=short_url)

    # When
    with pytest.raises(errors.CodeIsNotAvailable):
        fake_app.handle(requests.EncodeUrl(url="https://test.io"))

    # Then
    assert len(fake_app.repository.calls["add"]) == 1
    assert len(fake_app.repository.calls["get"]) == 1


def test_url_not_found(fake_app):
    # Given
    # Initial State (empty repository)

    # When
    with pytest.raises(errors.UrlNotFound):
        fake_app.handle(requests.DecodeShortenedUrl(code="test"))

    # Then
    assert len(fake_app.repository.calls["add"]) == 0
    assert len(fake_app.repository.calls["get"]) == 1


def test_unhandable_request(fake_app):
    # Given
    # Initial State (empty repository)

    # When
    with pytest.raises(NotImplementedError):
        fake_app.handle(requests.Request())

    # Then
    assert len(fake_app.repository.calls["add"]) == 0
    assert len(fake_app.repository.calls["get"]) == 0
