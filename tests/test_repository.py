from domain import model


def test_repository_add_and_get(fake_short_url_repository):
    entity = model.ShortUrlEntity(original_url="https://test.io", code="igokzx")
    fake_short_url_repository.add(entity=entity)
    actual = fake_short_url_repository.get(key="igokzx")
    assert actual.code == entity.code
    assert actual.original_url == entity.original_url


def test_repository_get_not_found(fake_short_url_repository):
    actual = fake_short_url_repository.get(key="igokzx")
    assert actual is None
