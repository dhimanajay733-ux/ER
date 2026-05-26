from __future__ import annotations

import time

from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.db.session_db import Base
from src.db.session_db import TimestampMixin



class Product(Base,TimestampMixin):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    price: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    sub_category_id: Mapped[int] = mapped_column(
        ForeignKey("subcategories.id"),
        nullable=False
    )

    seller_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    size: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    color: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    image_link: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    created_at: Mapped[int] = mapped_column(
        default=lambda: int(time.time())
    )

    updated_at: Mapped[int] = mapped_column(
        default=lambda: int(time.time()),
        onupdate=lambda: int(time.time())
    )
    # sub_category: Mapped["SubCategory"] = relationship(
    #     back_populates="products"
    # )