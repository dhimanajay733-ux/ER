from sqlalchemy import (
    String,
    ForeignKey,
    Boolean,
    Enum,
    BigInteger
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

from src.utils import (
    generate_uuid
)


class UserToken(TimestampMixin, Base):

    __tablename__ = "user_tokens"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=generate_uuid
    )

    user_id: Mapped[str] = mapped_column(
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

    expires_at: Mapped[int] = mapped_column(
        BigInteger
    )

    last_used_at: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True
    )