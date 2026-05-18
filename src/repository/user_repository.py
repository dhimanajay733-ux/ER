from sqlalchemy.orm import Session

from src.models.user_model import User

from src.schemas.user_schema import UserCreate


# GET USER BY EMAIL
def get_user_by_email(
    db: Session,
    email: str
):

    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


# GET USER BY ID
def get_user_by_id(
    db: Session,
    user_id: int
):

    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )


# CREATE USER
def create_user(
    db: Session,
    user_data: UserCreate,
    hashed_password: str
):

    new_user = User(

        first_name=user_data.first_name,

        last_name=user_data.last_name,

        email=user_data.email,

        password=hashed_password,

        # role=user_data.USER
    )

    db.add(new_user)

    db.flush()

    db.refresh(new_user)

    return new_user


# UPDATE USER
def update_user(
    db: Session,
    user: User
):

    db.add(user)

    db.flush()

    db.refresh(user)

    return user


# DELETE USER
def delete_user(
    db: Session,
    user: User
):

    db.delete(user)

    db.flush()