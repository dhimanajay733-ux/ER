import aiosmtplib
import time

from email.message import EmailMessage

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.config import settings

from src.repository.user_repository import (
    get_user_by_email,
    get_user_by_id
)
from fastapi import BackgroundTasks
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
async def send_otp_email(
    receiver: str,
    first_name:str,
    code: str
):

    msg = EmailMessage()

    msg.set_content(
        f"Thank you for joining with us {first_name}\nYour OTP verification code is: {code}"
    )

    msg["Subject"] = "OTP Verification"

    msg["From"] = settings.smtp_email

    msg["To"] = receiver

    await aiosmtplib.send(
        msg,
        hostname=settings.smtp_host,
        port=settings.smtp_port,
        username=settings.smtp_email,
        password=settings.smtp_password,
        use_tls=True,
    )

# GENERATE OTP SERVICE
async def generate_otp_service(
    db: AsyncSession,
    email: str,
    name:str,
    otp_type:str
):

    # GET USER
    user = await get_user_by_email(
        db,
        email
    )

    # CHECK USER
    if not user:

        raise UserNotFoundException()

    # GENERATE OTP
    otp_code = create_otp()

    # OTP EXPIRY (5 MINUTES)
    expires_at = int(time.time() * 1000) + (5 * 60 * 1000)
    # STORE OTP
    await create_otp_record(
        db=db,
        user_id=user.id,
        otp_code=otp_code,
        otp_type=otp_type,
        expires_at=expires_at
    )
    # SEND EMAIL
    await send_otp_email(
        email,
        name,
        otp_code
    )
       # COMMIT
    await db.commit()


    return {
        "message": "OTP sent successfully"
    }

# VERIFY OTP SERVICE
async def verify_otp_service(
    db: AsyncSession,
    user_id: str,
    otp_code: str
):

    # GET USER
    user = await get_user_by_id(
        db,
        user_id
    )

    # CHECK USER
    if not user:

        raise UserNotFoundException()

    # GET OTP
    otp_record = await get_valid_otp(
        db,
        user_id,
        otp_code
    )

    # CHECK EXPIRY
    if int(time.time()*1000) > otp_record.expires_at:

        raise OTPExpiredException()

    # MARK OTP USED
    await mark_otp_used(
        db,
        otp_record
    )

    # VERIFY USER
    user.is_verified = True

    await db.commit()

    return {
        "message": "OTP verified successfully"
    }