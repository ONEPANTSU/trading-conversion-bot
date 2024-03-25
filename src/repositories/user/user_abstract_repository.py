from abc import ABC, abstractmethod

from src.repositories.abstract_repository import AbstractRepository


class UserAbstractRepository(AbstractRepository, ABC):

    @abstractmethod
    async def get_by_language(self, language_code: str) -> list:
        raise NotImplementedError

    @abstractmethod
    async def get_with_privacy_by_language(self, language_code: str) -> list:
        raise NotImplementedError
