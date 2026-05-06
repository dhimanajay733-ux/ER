from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey

class OTPVerification:
    __tablename__ = "otp_verifications"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    otp_generated: Mapped[int] = mapped_column(Integer)

    type: Mapped[str] = mapped_column(String(50))

    status: Mapped[str] = mapped_column(
        String(20),
        default="pending"
    )