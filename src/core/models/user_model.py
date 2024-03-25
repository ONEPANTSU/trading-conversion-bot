from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models.annotated_types import int_pk
from src.core.models.base import Base
from src.core.utils.default_language_code import DEFAULT_LANGUAGE_CODE
from src.core.utils.default_roles import DEFAULT_ROLES_ID


class User(Base):
    __tablename__ = "user"

    id: Mapped[int_pk]
    username: Mapped[str]
    role_id: Mapped[int] = mapped_column(default=DEFAULT_ROLES_ID["user"])
    language_code: Mapped[str] = mapped_column(default=DEFAULT_LANGUAGE_CODE)
    privacy: Mapped[bool] = mapped_column(default=False)
