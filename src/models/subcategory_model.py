from sqlalchemy import (
    String,
    ForeignKey,
    Text
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from src.db.session_db import (
    Base,
    TimestampMixin
)


class SubCategory(
    TimestampMixin,
    Base
):

    __tablename__ = "subcategories"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    category_id = mapped_column(
        ForeignKey("categories.id")
    )
    type: Mapped[str] = mapped_column(
        String(50)
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )