from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

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

from src.services.token_service import (
    active_users,
    active_sessions
)

from src.core.logger import logger

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)

# REGISTER
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):

    logger.info(
        f"Received registration request: {user_data.email}"
    )

    user = await register_user(
        db=db,
        user_data=user_data
    )

    logger.info(
        f"User registered successfully: {user.email}"
    )

    return user


# LOGIN
@router.post("/login")
def login(
    user_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):

    logger.info(
        f"Received login request: {user_data.email}"
    )

    response = login_user(
        db=db,
        email=user_data.email,
        password=user_data.password
    )

    logger.info(
        f"User login successful: {user_data.email}"
    )

    return response


# ACTIVE USERS
@router.get("/active-users")
def get_active_users_route(
    db: AsyncSession = Depends(get_db)
):

    logger.info(
        "Fetching active users count"
    )

    total_users = active_users(db)

    return {
        "active_users": total_users
    }