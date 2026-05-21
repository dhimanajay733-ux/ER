from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from src.db.session_db import get_db

from src.schemas.otp_schema import VerifyOTPRequest

from src.services.otp_service import (
    generate_otp_service,
    verify_otp_service
)

from src.exceptions.otp_exception import (
    OTPGenerationException,
    OTPExpiredException,
    OTPInvalidException,
    EmailSendingException
    
)
from src.exceptions.user_exception import(
    UserNotFoundException
)

router = APIRouter(
    prefix="/api",
    tags=["OTP"]
)


#  GENERATE OTP
@router.post("/generate")
def generate_otp(
    email: str,
    db: Session = Depends(get_db)
):

    try:

        return generate_otp_service(
            db=db,
            email=email
        )

    except UserNotFoundException as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except OTPGenerationException as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    except EmailSendingException as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# VERIFY OTP
@router.post("/verify")
def verify_otp(
    user_data: VerifyOTPRequest,
    db: Session = Depends(get_db)
):

    try:

        return verify_otp_service(
            db=db,
            user_id=user_data.user_id,
            otp_code=user_data.otp_code
        )

    except OTPInvalidException as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except OTPExpiredException as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )