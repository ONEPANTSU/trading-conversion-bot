from src.repositories.repositories import Repositories
from src.services.admin_service import AdminService
from src.services.editor_service import EditorService
from src.services.user_service import UserService


class Services:
    def __init__(self, repositories: Repositories) -> None:
        self.user_service = UserService(repositories.user_repository)
        self.admin_service = AdminService(repositories.admin_repository)
        self.editor_service = EditorService(
            repositories.editor_repository, repositories.admin_repository
        )
