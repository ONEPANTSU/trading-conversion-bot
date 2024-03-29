from src.repositories.admin import AdminAbstractRepository
from src.services.users.user_service import UserService


class AdminService(UserService):
    repository: AdminAbstractRepository

    def __init__(self, repository: AdminAbstractRepository):
        super().__init__(repository)

    async def check_is_admin(self, user_id: int) -> bool:
        admins = [admin.id for admin in await self.repository.get_all()]
        return user_id in admins
