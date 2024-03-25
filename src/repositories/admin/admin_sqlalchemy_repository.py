from src.core.models import User
from src.core.utils.default_roles import DEFAULT_ROLES_ID
from src.repositories.admin.admin_abstract_repository import AdminAbstractRepository
from src.repositories.user import UserSQLAlchemyRepository


class AdminSQLAlchemyRepository(UserSQLAlchemyRepository, AdminAbstractRepository):
    model_table = User
    role_id = DEFAULT_ROLES_ID["admin"]
