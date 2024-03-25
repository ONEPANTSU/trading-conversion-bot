import uuid
from abc import ABC

from loguru import logger
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError

from src.core.models import User
from src.core.utils.default_roles import DEFAULT_ROLES_ID
from src.repositories.sqlalchemy_repository import SQLAlchemyRepository


class UserSQLAlchemyRepository(SQLAlchemyRepository, ABC):
    model_table = User
    role_id = DEFAULT_ROLES_ID["user"]

    async def create(self, model: model_table) -> int | uuid.UUID | IntegrityError:
        model.role_id = self.role_id
        return await super().create(model)

    async def update(self, model: model_table) -> None | IntegrityError:
        model.role_id = self.role_id
        return await super().update(model)

    async def get_by_language(self, language_code: str) -> list[User]:
        try:
            async with self.db.session_maker() as session:
                models = await session.execute(
                    select(self.model_table).filter(
                        self.model_table.role_id == self.role_id,
                        self.model_table.language_code == language_code,
                    )
                )
            rows = models.scalars().all()
            return rows
        except Exception as error:
            logger.error(str(error))
            raise error

    async def get_with_privacy_by_language(self, language_code: str) -> list[User]:
        try:
            async with self.db.session_maker() as session:
                models = await session.execute(
                    select(self.model_table).filter(
                        self.model_table.role_id == self.role_id,
                        self.model_table.language_code == language_code,
                        self.model_table.privacy,
                    )
                )
            rows = models.scalars().all()
            return rows
        except Exception as error:
            logger.error(str(error))
            raise error

    async def get_all(self) -> list[model_table] | Exception:
        try:
            async with self.db.session_maker() as session:
                models = await session.execute(
                    select(self.model_table).filter(
                        self.model_table.role_id == self.role_id
                    )
                )
            rows = models.scalars().all()
            return rows
        except Exception as error:
            logger.error(str(error))
            raise error

    async def delete_all(self) -> None | IntegrityError:
        try:
            async with self.db.session_maker() as session:
                await session.execute(
                    delete(self.model_table).filter(
                        self.model_table.role_id == self.role_id
                    )
                )
                await session.commit()
        except IntegrityError as error:
            logger.error(str(error))
            raise error
