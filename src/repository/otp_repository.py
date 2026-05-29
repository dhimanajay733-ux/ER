from sqlalchemy.orm import Session

from src.models.otp_model import OTPVerification

from src.exceptions.otp_exception import (
    OTPGenerationException,
    OTPInvalidException
)

# CREATE OTP RECORD
def create_otp_record(
    db: Session,
    user_id: int,
    otp_code: str,
    otp_type: str,
    expires_at
):
    
    try:

        new_otp = OTPVerification(

            user_id=user_id,

            otp_code=otp_code,

            otp_type=otp_type,

            expires_at=expires_at,

            is_used=False
        )

        db.add(new_otp)

        db.flush()

        db.refresh(new_otp)

        return new_otp

    except Exception as e:

        db.rollback()

        raise OTPGenerationException(
            str(e)
        )


# GET VALID OTP
def get_valid_otp(
    db: Session,
    user_id: str,
    otp_code: str
):

    try:

        otp_record = (
            db.query(OTPVerification)
            .filter(
                OTPVerification.user_id == user_id,
                OTPVerification.otp_code == otp_code,
                OTPVerification.is_used == False
            )
            .first()
        )

        if not otp_record:

            raise OTPInvalidException()

        return otp_record

    except Exception as e:

        raise e


# MARK OTP AS USED
def mark_otp_used(
    db: Session,
    otp_record: OTPVerification
):

    try:

        otp_record.is_used = True

        db.add(otp_record)

        db.flush()

        db.refresh(otp_record)

        return otp_record

    except Exception as e:

        db.rollback()

        raise e