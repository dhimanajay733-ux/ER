from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.db.session_db import get_db
from src.schemas.user_schema import (
    UserCreate,
    UserResponse,
    UserLogin
)

from src.services.user_service import (
    register_user,
    login_user
)


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)


# =========================
# REGISTER
# =========================
@router.post(
    "/register",
    response_model=UserResponse
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):

    return register_user(
        db=db,
        user_data=user_data
    )


# =========================
# LOGIN
# =========================
@router.post("/login")
def login(
    user_data: UserLogin,
    db: Session = Depends(get_db)
):

    return login_user(
        db=db,
        email=user_data.email,
        password=user_data.password
    )