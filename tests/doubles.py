from __future__ import annotations

from typing import TypeVar, Union

from application import repository
from domain import model

E = TypeVar("E", bound=model.Entity)


class AbstractInMemoryRepository(repository.AbstractRepository[E]):
    data: dict[str, E] = {}

    def add(self, entity: E) -> None:
        raise NotImplementedError

    def get(self, key: str) -> Union[None, E]:
        if key in self.data:
            return self.data[key]

        return None


class FakeShortUrlRepository(
    AbstractInMemoryRepository[model.ShortUrlEntity], repository.ShortUrlRepository
):
    def add(self, entity: model.ShortUrlEntity) -> None:
        self.data[entity.code] = entity
