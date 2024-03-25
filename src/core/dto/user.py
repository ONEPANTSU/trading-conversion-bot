from dataclasses import dataclass

from src.core.utils.default_language_code import DEFAULT_LANGUAGE_CODE
from src.core.utils.default_roles import DEFAULT_ROLES_ID


@dataclass
class User:
    id: int
    username: str
    role_id: int = DEFAULT_ROLES_ID["user"]
    language_code: str = DEFAULT_LANGUAGE_CODE
    privacy: bool = False
