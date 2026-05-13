from datetime import datetime
from sqlalchemy import String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from src.db.session_db import Base


class OTPVerification(Base):
    __tablename__ = "otp_verifications"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    otp_code: Mapped[str] = mapped_column(  
        String(6)
    )
 
    otp_type: Mapped[str] = mapped_column(
        String(20)
    )

    is_used: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )  

    expires_at: Mapped[datetime] = mapped_column()

