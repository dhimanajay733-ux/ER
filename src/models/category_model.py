from sqlalchemy import (
    String,
    Text
)

from sqlalchemy.orm import Mapped, mapped_column
from src.db.session_db import Base ,TimestampMixin

class Category(Base,TimestampMixin):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

