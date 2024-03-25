from src.core.models import User
from src.core.utils.default_roles import DEFAULT_ROLES_ID
from src.repositories.editor import EditorAbstractRepository
from src.repositories.user import UserSQLAlchemyRepository


class EditorSQLAlchemyRepository(
    UserSQLAlchemyRepository, EditorAbstractRepository
):
    model_table = User
    role_id = DEFAULT_ROLES_ID["editor"]
