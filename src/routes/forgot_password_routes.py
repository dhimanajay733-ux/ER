from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from sqlalchemy.orm import Session
from src.schemas.forgot_password_schema import (
    ForgotPasswordRequest,
    ResetPasswordRequest
)
from src.db.session_db import get_db
from src.services.forgot_password_service import (
    forgot_password_service,
    reset_password_service
)
router=APIRouter()


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


@router.post("/forgot-password")
def forgot_password(
    user_data: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):

    return forgot_password_service(
        db=db,
        email=user_data.email
    )

# @router.post("/reset-password")
# def reset_password(
#     user_data: ResetPasswordRequest,
#     db: Session = Depends(get_db)
# ):

#     return reset_password_service(
#         db=db,
#         user_id=user_data.user_id,
#         otp_code=user_data.otp_code,
#         new_password=user_data.new_password,
#         confirm_password=user_data.confirm_password
#     )