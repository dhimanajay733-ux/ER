from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.schemas.forgot_password_schema import (
    ResetPasswordRequest
)
from src.services.reset_password_service import (
    reset_password_service
)
from src.db.session_db import get_db
router = APIRouter()


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


@router.post("/reset-password")
def reset_password(
    user_data: ResetPasswordRequest,
    db: Session = Depends(get_db)
):

    return reset_password_service(
        db=db,
        user_id=user_data.user_id,
        otp_code=user_data.otp_code,
        new_password=user_data.new_password,
        confirm_password=user_data.confirm_password
    )