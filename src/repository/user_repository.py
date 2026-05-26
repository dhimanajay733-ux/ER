from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from src.models.user_model import User

from src.schemas.user_schema import UserCreate

from src.exceptions.database_exception import (
    DatabaseInsertException,
    DatabaseFetchException,
    DatabaseUpdateException
)

# GET USER BY EMAIL
def get_user_by_email(
    db: Session,
    email: str
):

    try:

        return (
            db.query(User)
            .filter(User.email == email)
            .first()
        )
    except Exception as e:

        raise DatabaseFetchException


# GET USER BY ID
def get_user_by_id(
    db: Session,
    user_id: int
):

    try:

        return (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    except Exception as e:

        raise DatabaseFetchException


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

        print(e)

        raise e

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

        raise DatabaseUpdateException

# DELETE USER
def delete_user(
    db: Session,
    user: User
):

    try:

        db.delete(user)

        db.flush()

    except Exception as e:

        db.rollback()

        raise DatabaseUpdateException
    


