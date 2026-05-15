from datetime import datetime

from sqlalchemy import (
    String,
    ForeignKey,
    Boolean,
    DateTime,
    Enum
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from src.db.session_db import (
    Base,
    TimestampMixin
)

from src.enums.token_enum import TokenType


class UserToken(TimestampMixin, Base):

    __tablename__ = "user_tokens"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    jti: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True
    )

    parent_jti: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    token_type: Mapped[TokenType] = mapped_column(
        Enum(TokenType)
    )

    is_revoked: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime
    )

    last_used_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )