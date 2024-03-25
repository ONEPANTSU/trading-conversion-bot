from src.core.database import DataBase
from src.repositories.admin import AdminSQLAlchemyRepository
from src.repositories.editor import EditorSQLAlchemyRepository
from src.repositories.user import UserSQLAlchemyRepository


class Repositories:

    def __init__(self, database: DataBase) -> None:
        self.user_repository = UserSQLAlchemyRepository(database)
        self.editor_repository = EditorSQLAlchemyRepository(database)
        self.admin_repository = AdminSQLAlchemyRepository(database)
