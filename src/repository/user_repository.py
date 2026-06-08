from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.user_model import User

from src.schemas.user_schema import UserCreate

from src.exceptions.database_exception import (
    DatabaseInsertException,
    DatabaseFetchException,
    DatabaseUpdateException
)

from src.core.logger import logger


# GET USER BY EMAIL
async def get_user_by_email(
    db: AsyncSession,
    email: str
):

    try:
        stmt = select(User).where(User.email == email)
        result= await db.execute(stmt)
        user= result.scalar_one_or_none()

        return user

    except Exception as e:

        logger.error(
            f"Failed to fetch user by email: {str(e)}"
        )

        raise DatabaseFetchException()


# GET USER BY ID
async def get_user_by_id(
    db: AsyncSession,
    user_id: int
):

    try:
        stmt = select(User).where(User.id == user_id)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none

        return user

    except Exception as e:

        logger.error(
            f"Failed to fetch user by id: {str(e)}"
        )

        raise DatabaseFetchException()


# CREATE USER
async def create_user(
    db: AsyncSession,
    user_data: UserCreate,
    hashed_password: str
):

    try:

        new_user = User(

            first_name=user_data.first_name,

            last_name=user_data.last_name,

            email=user_data.email,

            password=hashed_password
        )

        db.add(new_user)
       
        await db.flush()

        await db.refresh(new_user)

        return new_user

    except Exception as e:

        logger.error(
            f"Failed to create user: {str(e)}"
        )

        raise DatabaseInsertException()


# UPDATE USER
async def update_user(
    db: AsyncSession,
    user: User
):

    try:

        await db.flush()

        await db.refresh(user)

        return user

    except Exception as e:

        db.rollback()

        logger.error(
            f"Failed to update user: {str(e)}"
        )

        raise DatabaseUpdateException()


# DELETE USER
async def delete_user(
    db: AsyncSession,
    user: User
):

    try:

        await db.delete(user)

        await db.flush()

        return True

    except Exception as e:

        await db.rollback()

        logger.error(
            f"Failed to delete user: {str(e)}"
        )

        raise DatabaseUpdateException()