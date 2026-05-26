from fastapi import HTTPException, status, APIRouter, Depends
from src.services.otp_service import generate_otp_service
from src.db.session_db import get_db
from sqlalchemy.orm import Session
from src.services.otp_service import generate_otp_service
from src.exceptions.otp_exception import(
    OTPGenerationException
)
from src.exceptions.user_exception import(
    UserNotFoundException
)
router= APIRouter

router = APIRouter(
    prefix="/api/auth",
    tags=["OTP"]
)


@router.post("/Resend_Otp") 
def generate_otp(
    email: str,
    db: Session = Depends(get_db)
    ):

    try:
        return generate_otp_service(
            db=db,
            email=email,
            otp_type='Resend_Otp'
        )

    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

    except OTPGenerationException as e:
        raise HTTPException(status_code=500, detail=str(e))