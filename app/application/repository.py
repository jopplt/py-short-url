from typing import Any, Generic, TypeVar, Union

from domain import model

E = TypeVar("E", bound=model.Entity)


class AbstractRepository(Generic[E]):
    def add(self, entity: E) -> None:  # pragma: no cover
        raise NotImplementedError

    def get(self, key: Any) -> E:  # pragma: no cover
        raise NotImplementedError


class ShortUrlRepository(AbstractRepository[model.ShortUrlEntity]):
    def add(self, entity: model.ShortUrlEntity) -> None:  # pragma: no cover
        raise NotImplementedError

    def get(self, key: str) -> Union[None, model.ShortUrlEntity]:  # pragma: no cover
        raise NotImplementedError
