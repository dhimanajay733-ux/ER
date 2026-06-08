from sqlalchemy.ext.asyncio import AsyncSession

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

from src.core.logger import logger


# REGISTER USER
async def register_user(
    db: AsyncSession,
    user_data: UserCreate
):

    logger.info(
        f"Checking existing user: {user_data.email}"
    )

    # CHECK USER EXISTS
    existing_user = await get_user_by_email(
        db,
        user_data.email
    )

    if existing_user:

        logger.warning(
            f"User already exists: {user_data.email}"
        )

        raise UserAlreadyExistsException()

    logger.info(
        f"Hashing password for: {user_data.email}"
    )

    # HASH PASSWORD
    hashed_password = hash_password(
        user_data.password
    )

    try:

        logger.info(
            f"Creating user: {user_data.email}"
        )

        # CREATE USER
        new_user = await create_user(
            db=db,
            user_data=user_data,
            hashed_password=hashed_password
        )

        # COMMIT USER
        db.commit()

        logger.info(
            f"User committed successfully: {new_user.email}"
        )

        # GENERATE OTP
        await generate_otp_service(
            db=db,
            email=new_user.email,
            name=new_user.first_name,
            otp_type="Email_Verification"
        )

        logger.info(
            f"OTP generated successfully: {new_user.email}"
        )

        return new_user

    except Exception as e:

        db.rollback()

        logger.error(
            f"User registration failed: {str(e)}"
        )

        raise e


# LOGIN USER
async def login_user(
    db: AsyncSession,
    email: str,
    password: str
):

    logger.info(
        f"Fetching user for login: {email}"
    )

    # GET USER
    user = await get_user_by_email(
        db,
        email
    )

    # CHECK USER EXISTS
    if not user:

        logger.warning(
            f"Invalid login email: {email}"
        )

        raise InvalidCredentialsException()

    # CHECK VERIFIED
    if not user.is_verified:

        logger.warning(
            f"Unverified user login attempt: {email}"
        )

        raise UserNotVerifiedException()

    logger.info(
        f"Verifying password: {email}"
    )

    # VERIFY PASSWORD
    is_valid_password = await verify_password(
        password,
        user.password
    )

    if not is_valid_password:

        logger.warning(
            f"Invalid password attempt: {email}"
        )

        raise InvalidCredentialsException()

    logger.info(
        f"Generating JTI for: {email}"
    )

    # GENERATE JTI
    jti = await generate_jti()

    logger.info(
        f"Generating access token: {email}"
    )

    # CREATE ACCESS TOKEN
    access_token = await create_access_token(
        user.id,
        jti
    )

    logger.info(
        f"Login successful: {email}"
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }