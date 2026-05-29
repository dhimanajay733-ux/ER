from sqlalchemy import (
    String,
    Float,
    Integer,
    Text,
    ForeignKey
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from src.db.session_db import (
    Base,
    TimestampMixin
)

class Product(
    TimestampMixin,
    Base
):

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    slug: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
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

    seller_id: Mapped[str] = mapped_column(
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
        String(255),
        nullable=True
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    subcategory = relationship(
        "SubCategory",
        back_populates="products"
    )