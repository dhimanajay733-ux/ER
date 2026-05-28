from sqlalchemy.orm import Session

from src.models.user_model import User

from src.schemas.user_schema import UserCreate

from src.exceptions.database_exception import (
    DatabaseInsertException,
    DatabaseFetchException,
    DatabaseUpdateException
)

from src.core.logger import logger


# GET USER BY EMAIL
def get_user_by_email(
    db: Session,
    email: str
):

    try:

        query = (
            db.query(User)
            .filter(User.email == email)
        )

        user = query.first()

        return user

    except Exception as e:

        logger.error(
            f"Failed to fetch user by email: {str(e)}"
        )

        raise DatabaseFetchException()


# GET USER BY ID
def get_user_by_id(
    db: Session,
    user_id: int
):

    try:

        query = (
            db.query(User)
            .filter(User.id == user_id)
        )

        user = query.first()

        return user

    except Exception as e:

        logger.error(
            f"Failed to fetch user by id: {str(e)}"
        )

        raise DatabaseFetchException()


# CREATE USER
def create_user(
    db: Session,
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

        db.flush()

        db.refresh(new_user)

        return new_user

    except Exception as e:

        logger.error(
            f"Failed to create user: {str(e)}"
        )

        raise DatabaseInsertException()


# UPDATE USER
def update_user(
    db: Session,
    user: User
):

    try:

        db.add(user)

        db.flush()

        db.refresh(user)

        return user

    except Exception as e:

        db.rollback()

        logger.error(
            f"Failed to update user: {str(e)}"
        )

        raise DatabaseUpdateException()


# DELETE USER
def delete_user(
    db: Session,
    user: User
):

    try:

        db.delete(user)

        db.flush()

        return True

    except Exception as e:

        db.rollback()

        logger.error(
            f"Failed to delete user: {str(e)}"
        )

        raise DatabaseUpdateException()