from abc import ABC

from src.repositories.abstract_repository import AbstractRepository


class AbstractService(ABC):
    def __init__(
        self,
        repository: AbstractRepository,
    ):
        self.repository = repository
        self.model_table = repository.model_table
