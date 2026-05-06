from datetime import datetime
from typing import List
from src.models import f,e,password,is_active
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean

class User:
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    first_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True)

    password: Mapped[str] = mapped_column(String(255))

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)