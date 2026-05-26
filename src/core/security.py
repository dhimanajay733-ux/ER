from datetime import datetime, timedelta, timezone
import uuid

from jose import jwt
from passlib.context import CryptContext

from src.core.config import settings

# GENERATE JTI
def generate_jti() -> str:

    return str(uuid.uuid4())


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
    user_id: str,
    jti: str,
    role:str
) -> str:

    expire = datetime.now(
        timezone.utc
    ) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload = {
        "sub": str(user_id),
        "jti": jti,
        "exp": expire,
        "role": role
    }

    token = jwt.encode(
        payload,
        settings.jwt_secret.get_secret_value(),
        algorithm=settings.jwt_algorithm
    )

    return token