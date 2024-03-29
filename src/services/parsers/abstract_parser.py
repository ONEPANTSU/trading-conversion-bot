from abc import ABC, abstractmethod


class AbstractParser(ABC):
    @abstractmethod
    def check_registration(self, uuid: str):
        raise NotImplementedError
