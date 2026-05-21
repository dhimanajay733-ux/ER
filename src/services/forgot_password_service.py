import time
from sqlalchemy.orm import Session

from src.repository.user_repository import (
    get_user_by_email,
    get_user_by_id,
    update_user
)
from src.repository.otp_repository import (
    get_valid_otp,
    mark_otp_used
)
from src.services.otp_service import (
    generate_otp_service
)

from src.core.security import (
    hash_password
)

from src.exceptions.user_exception import (
    UserNotFoundException
)
from src.exceptions.otp_exception import (
    OTPExpiredException,
    OTPInvalidException
)


# FORGOT PASSWORD SERVICE
def forgot_password_service(
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
    return generate_otp_service(
        db=db,
        email=user.email,
        otp_type="FORGOT_PASSWORD"
    )


# RESET PASSWORD SERVICE
def reset_password_service(
    db: Session,
    user_id: str,
    otp_code: str,
    new_password: str,
    confirm_password: str
):

    # CHECK PASSWORD MATCH
    if new_password != confirm_password:

        raise Exception(
            "Passwords do not match"
        )

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
        user.id,
        otp_code
    )

    # CHECK OTP
    if not otp_record:

        raise OTPInvalidException()

    # CHECK OTP EXPIRY
    if int(time.time() * 1000) > otp_record.expires_at:

        raise OTPExpiredException()

    # HASH PASSWORD
    hashed_password = hash_password(
        new_password
    )

    # UPDATE PASSWORD
    user.password = hashed_password

    # MARK OTP USED
    mark_otp_used(
        db,
        otp_record
    )

    # UPDATE USER
    update_user(
        db,
        user
    )

    # COMMIT
    db.commit()

    return {
        "message": "Password reset successful"
    }