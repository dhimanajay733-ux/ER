from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, Enum

from src.enums.user_enum import UserRole

from src.db.session_db import Base, TimestampMixin


class User(TimestampMixin, Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    first_name: Mapped[str] = mapped_column(
        String(100)
    )

    last_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True
    )

    password: Mapped[str] = mapped_column(
        String(255)
    )

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        default=UserRole.USER
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )
    is_verified: Mapped[bool] = mapped_column(
    Boolean,
    default=False
)