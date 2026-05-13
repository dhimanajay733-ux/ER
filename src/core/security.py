from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext
# from passlib import crypto
from src.core.config import settings


# PASSWORD HASHING CONTEXT
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# HASH PASSWORD
def hash_password(password: str) -> str:

    return pwd_context.hash(password)


# VERIFY PASSWORD
def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# CREATE ACCESS TOKEN
def create_access_token(
    user_id: int
) -> str:

    expire = datetime.now(
        timezone.utc
    ) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload = {
        "sub": str(user_id),
        "exp": expire
    }

    token = jwt.encode(
        payload,
        settings.jwt_secret.get_secret_value(),
        algorithm=settings.jwt_algorithm
    )

    return token