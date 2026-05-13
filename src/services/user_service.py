from sqlalchemy.orm import Session

from src.repository.user_repository import get_user_by_email,get_user_by_id,update_user,delete_user


from src.schemas.user_schema import UserCreate

from src.core.security import (
    hash_password,
    verify_password,
    create_access_token
)


# REGISTER USER
def register_user(
    db: Session,
    user_data: UserCreate
):
    
    # CHECK IF USER EXISTS
    existing_user = get_user_by_email(
        db,
        user_data.email
    )

    if existing_user:
        raise ValueError(
            "User with this email already exists"
        )

    # HASH PASSWORD
    hashed_password = hash_password(
        user_data.password
    )

    try:

        # CREATE USER
        new_user = create_user(
            db=db,
            user_data=user_data,
            hashed_password=hashed_password
        )

        # COMMIT TRANSACTION
        db.commit()

        return new_user

    except Exception as e:

        # ROLLBACK IF ERROR
        db.rollback()

        raise e


# LOGIN USER
def login_user(
    db: Session,
    email: str,
    password: str
):

    # GET USER
    user = get_user_by_email(
        db,
        email
    )

    # CHECK USER EXISTS
    if not user:
        raise ValueError(
            "Invalid email or password"
        )

    # VERIFY PASSWORD
    is_valid_password = verify_password(
        password,
        user.password
    )

    if not is_valid_password:
        raise ValueError(
            "Invalid email or password"
        )

    # CREATE ACCESS TOKEN
    access_token = create_access_token(
        user.id
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }