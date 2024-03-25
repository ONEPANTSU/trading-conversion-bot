from src.repositories.admin import AdminAbstractRepository
from src.repositories.editor import EditorAbstractRepository
from src.services.user_service import UserService


class EditorService(UserService):
    repository: EditorAbstractRepository

    def __init__(
        self,
        repository: EditorAbstractRepository,
        admin_repository: AdminAbstractRepository,
    ):
        super().__init__(repository)
        self.admin_repository = admin_repository

    async def check_is_editor(self, user_id: str) -> bool:
        editors = [editor.id for editor in await self.repository.get_all()] + [
            admin.id for admin in await self.admin_repository.get_all()
        ]
        return user_id in editors
