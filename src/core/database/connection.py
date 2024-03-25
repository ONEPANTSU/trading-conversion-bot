from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

from src.core.config.config import DataBaseConfig


class Connection:
    def __init__(self, db_config: DataBaseConfig):
        self.db = db_config
        self.engine = self.__create_engine()

    def get_url(self) -> str:
        return (
            f"{self.db.driver}://"
            f"{self.db.user}:{self.db.password}@"
            f"{self.db.host}:{self.db.port}/{self.db.name}"
        )

    def __create_engine(self):
        return create_async_engine(url=self.get_url(), poolclass=NullPool)
