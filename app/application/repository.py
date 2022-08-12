from typing import Any, Generic, TypeVar

from domain import model

E = TypeVar("E", bound=model.Entity)


class AbstractRepository(Generic[E]):
    def add(self, entity: E) -> None:
        raise NotImplementedError

    def get(self, key: Any) -> E:
        raise NotImplementedError


class ShortUrlRepository(AbstractRepository[model.ShortUrlEntity]):
    def add(self, entity: model.ShortUrlEntity) -> None:
        raise NotImplementedError

    def get(self, key: str) -> model.ShortUrlEntity:
        raise NotImplementedError
