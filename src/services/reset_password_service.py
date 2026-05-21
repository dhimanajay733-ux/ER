import time 
from src.utils import create_otp
from src.repository.user_repository import (
    get_user_by_id
)
from src.repository.otp_repository import (
    mark_otp_used,
    get_valid_otp
)
from src.repository.user_repository import (
    update_user
)
from sqlalchemy.orm import Session
from src.repository.otp_repository import get_valid_otp
from src.exceptions.user_exception import (
    UserNotFoundException
)
from src.exceptions.otp_exception import (
    OTPExpiredException,
    OTPInvalidException
)
from src.core.security import (
    hash_password
)


def reset_password_service(
    db:Session,
    user_id:str,
    otp_code:str,
    new_password:str,
    confirm_password:str    
):
    if new_password != confirm_password:

        raise Exception(
            "Passwords do not match"
        )

 #   otp_code=create_otp()
    user=get_user_by_id(
        db,
        user_id
    )
    # User Exists?
    if not user:

        raise UserNotFoundException()

    # GET OTP
    otp_record = get_valid_otp(
        db,
        user.id,
        otp_code
    )
    if not otp_record:

        raise OTPInvalidException()

    # IS EXPIRED?
    if int(time.time() * 1000) > otp_record.expires_at:

        raise OTPExpiredException()

    # HASH PASSWORD
    hashed_password = hash_password(
        new_password
    )

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


    
    