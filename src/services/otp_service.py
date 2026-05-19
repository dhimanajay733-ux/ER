import smtplib
import time

from email.message import EmailMessage

from sqlalchemy.orm import Session

from src.core.config import settings

from src.repository.user_repository import (
    get_user_by_email,
    get_user_by_id
)

from src.repository.otp_repository import (
    create_otp_record,
    get_valid_otp,
    mark_otp_used
)

from src.utils import (
    create_otp
)

from src.exceptions.user_exception import (
    UserNotFoundException
)

from src.exceptions.otp_exception import (
    OTPExpiredException
)


# SEND OTP EMAIL
def send_otp_email(
    receiver: str,
    code: str
):

    msg = EmailMessage()

    msg.set_content(
        f"Your OTP verification code is: {code}"
    )

    msg["Subject"] = "OTP Verification"

    msg["From"] = settings.smtp_email

    msg["To"] = receiver

    with smtplib.SMTP_SSL(
        settings.smtp_host,
        settings.smtp_port
    ) as server:

        server.login(
            settings.smtp_email,
            settings.smtp_password
        )

        server.send_message(msg)


# GENERATE OTP SERVICE
def generate_otp_service(
    db: Session,
    email: str
):

    # GET USER
    user = get_user_by_email(
        db,
        email
    )

    # CHECK USER
    if not user:

        raise UserNotFoundException()

    # GENERATE OTP
    otp_code = create_otp()

    # OTP EXPIRY (5 MINUTES)
    expires_at = int(time.time()) + 300

    # STORE OTP
    create_otp_record(
        db=db,
        user_id=user.id,
        otp_code=otp_code,
        otp_type="EMAIL_VERIFICATION",
        expires_at=expires_at
    )

    # COMMIT
    db.commit()

    # SEND EMAIL
    send_otp_email(
        email,
        otp_code
    )

    return {
        "message": "OTP sent successfully"
    }


# VERIFY OTP SERVICE
def verify_otp_service(
    db: Session,
    user_id: str,
    otp_code: str
):

    # GET USER
    user = get_user_by_id(
        db,
        user_id
    )

    # CHECK USER
    if not user:

        raise UserNotFoundException()

    # GET OTP
    otp_record = get_valid_otp(
        db,
        user_id,
        otp_code
    )

    # CHECK EXPIRY
    if int(time.time()) > otp_record.expires_at:

        raise OTPExpiredException()

    # MARK OTP USED
    mark_otp_used(
        db,
        otp_record
    )

    # VERIFY USER
    user.is_verified = True

    db.add(user)

    db.commit()

    return {
        "message": "OTP verified successfully"
    }