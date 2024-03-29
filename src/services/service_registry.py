from src.core.config.parsers.parser_config import ParserConfig
from src.repositories.repository_registry import RepositoryRegistry
from src.services.parsers.parsing_service import ParsingService
from src.services.users.admin_service import AdminService
from src.services.users.editor_service import EditorService
from src.services.users.user_service import UserService


class ServiceRegistry:
    def __init__(
        self, repositories: RepositoryRegistry, parser_config: ParserConfig
    ) -> None:
        self.user_service = UserService(repositories.user_repository)
        self.admin_service = AdminService(repositories.admin_repository)
        self.editor_service = EditorService(
            repositories.editor_repository, repositories.admin_repository
        )
        self.parsing_service = ParsingService(parser_config)
