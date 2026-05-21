from sqlalchemy.orm import Session

from src.repository.user_repository import (
    get_user_by_email,
    create_user
)

from src.schemas.user_schema import UserCreate

from src.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    generate_jti
)

from src.exceptions.user_exception import (
    UserNotVerifiedException,
    UserAlreadyExistsException,
    InvalidCredentialsException
)

from src.services.otp_service import (
    generate_otp_service
)

# REGISTER USER
def register_user(
    db: Session,
    user_data: UserCreate
):
    
    #CHECK ID USER EXISTS
    existing_user = get_user_by_email(
        db,
        user_data.email
    )

    if existing_user:

        raise UserAlreadyExistsException()

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

        # COMMIT USER
        db.commit()

        # GENERATE OTP
        generate_otp_service(
            db=db,
            email=new_user.email,
            otp_type="Email_Verification"
        )

        return new_user

    except Exception as e:
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

        raise InvalidCredentialsException()

    # CHECK VERIFIED
    if not user.is_verified:

        raise UserNotVerifiedException()

    # VERIFY PASSWORD
    is_valid_password = verify_password(
        password,
        user.password
    )

    if not is_valid_password:

        raise InvalidCredentialsException()

    # GENERATE JTI
    jti = generate_jti()

    # CREATE ACCESS TOKEN
    access_token = create_access_token(
        user.id,
        jti
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }