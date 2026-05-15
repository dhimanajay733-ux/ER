from datetime import datetime, timezone

from sqlalchemy.orm import Session

from src.models.token_model import UserToken

from src.enums.token_enum import TokenType

# CREATE USER TOKEN
def create_user_token(
    db: Session,
    user_id: int,
    jti: str,
    token_type: TokenType,
    expires_at: datetime,
    parent_jti: str | None = None
):

    new_token = UserToken(

        user_id=user_id,

        jti=jti,

        parent_jti=parent_jti,

        token_type=token_type,

        expires_at=expires_at,

        is_revoked=False,

        last_used_at=datetime.now(timezone.utc)
    )

    db.add(new_token)

    db.flush()

    db.refresh(new_token)

    return new_token


# GET TOKEN BY JTI
def get_token_by_jti(
    db: Session,
    jti: str
):

    return (
        db.query(UserToken)
        .filter(UserToken.jti == jti)
        .first()
    )


# REVOKE TOKEN
def revoke_token(
    db: Session,
    token: UserToken
):

    token.is_revoked = True

    db.add(token)

    db.flush()

    db.refresh(token)

    return token

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from src.models.token_model import UserToken


def get_active_sessions_count(
    db: Session
):

    return (
        db.query(UserToken)
        .filter(
            UserToken.is_revoked == False,
            UserToken.expires_at > datetime.now(timezone.utc)
        )
        .count()
    )

from sqlalchemy import distinct


def get_active_users_count(
    db: Session
):

    return (
        db.query(
            distinct(UserToken.user_id)
        )
        .filter(
            UserToken.is_revoked == False,
            UserToken.expires_at > datetime.now(timezone.utc)
        )
        .count()
    )