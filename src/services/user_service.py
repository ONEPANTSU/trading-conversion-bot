import uuid
from dataclasses import asdict

from src.core.dto.user import User
from src.core.utils.default_language_code import DEFAULT_LANGUAGE_CODE
from src.repositories.user import UserAbstractRepository
from src.services.abstract_service import AbstractService


class UserService(AbstractService):
    repository: UserAbstractRepository

    def __init__(self, repository: UserAbstractRepository):
        super().__init__(repository)

    async def get_user(self, user_id) -> User | None:
        model = await self.repository.get(user_id)
        if model:
            return User(**model.get_dict())
        return None

    async def get_users(self) -> list[User]:
        models = await self.repository.get_all()
        return [User(**user.get_dict()) for user in models]

    async def get_users_by_language(self, language_code: str) -> list[User]:
        models = await self.repository.get_by_language(language_code)
        return [User(**user.get_dict()) for user in models]

    async def get_users_with_privacy_by_language(self, language_code: str) -> list[User]:
        models = await self.repository.get_with_privacy_by_language(language_code)
        return [User(**user.get_dict()) for user in models]

    async def create_user(self, user: User) -> None:
        if user.language_code == "":
            user.language_code = DEFAULT_LANGUAGE_CODE
        db_user = await self.get_user(user.id)
        if not db_user:
            await self.repository.create(self.model_table(**asdict(user)))
        elif user != db_user:
            await self.repository.update(self.model_table(**asdict(user)))

    async def update_user(self, user: User) -> None:
        if user.language_code == "":
            user.language_code = DEFAULT_LANGUAGE_CODE
        await self.repository.update(self.model_table(**asdict(user)))

    async def delete_user(self, user_id: int | uuid.UUID) -> None:
        await self.repository.delete(user_id)
