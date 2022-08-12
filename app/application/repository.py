import abc
from typing import Any


class AbstractRepository(abc.ABC):
    from domain.model import Entity

    @abc.abstractmethod
    def add(self, entity: Entity) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, key: Any) -> Entity:
        raise NotImplementedError


class ShortUrlRepository(AbstractRepository):
    from domain.model import ShortUrlEntity

    @abc.abstractmethod
    def add(self, entity: ShortUrlEntity) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, key: str) -> ShortUrlEntity:
        raise NotImplementedError
