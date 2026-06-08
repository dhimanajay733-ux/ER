from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.otp_model import OTPVerification
from sqlalchemy import select
from src.exceptions.otp_exception import (
    OTPGenerationException,
    OTPInvalidException
)

# CREATE OTP RECORD
async def create_otp_record(
    db: AsyncSession,
    user_id: int,
    otp_code: str,
    otp_type: str,
    expires_at
):
    
    try:
 
        new_otp =  OTPVerification(

            user_id=user_id,

            otp_code=otp_code,

            otp_type=otp_type,

            expires_at=expires_at,

            is_used=False
        )
        db.add(new_otp)

        await db.flush()

        await db.refresh(new_otp)

        return new_otp

    except Exception as e:

        await db.rollback()

        raise OTPGenerationException(
            str(e)
        )


# GET VALID OTP
async def get_valid_otp(
    db: AsyncSession,
    user_id: str,
    otp_code: str
):

    try:
        stmt = select(OTPVerification
        ).where(
                OTPVerification.user_id == user_id,
                OTPVerification.otp_code == otp_code,
                OTPVerification.is_used == False
            )
        result = await db.execute(stmt)
        otp_record = result.scalar_one_or_none()
        
        if not otp_record:

            raise OTPInvalidException()

        return otp_record

    except Exception as e:

        raise e


# MARK OTP AS USED
async def mark_otp_used(
    db: AsyncSession,
    otp_record: OTPVerification
):

    try:

        otp_record.is_used = True

        await db.flush()

        await db.refresh(otp_record)

        return otp_record

    except Exception as e:

        await db.rollback()

        raise e