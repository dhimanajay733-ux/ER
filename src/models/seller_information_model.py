from sqlalchemy import (
    String,
    ForeignKey,
    Boolean
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from src.db.session_db import (
    Base,
    TimestampMixin
)


class SellerInformation(
    TimestampMixin,
    Base
):

    __tablename__ = "seller_information"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    store_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True
    )

    status: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )