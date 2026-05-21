from sqlalchemy.orm import Session

from sqlalchemy import distinct, func

import time

from src.models.token_model import UserToken

from src.enums.token_enum import TokenType


# CREATE USER TOKEN
def create_user_token(
    db: Session,
    user_id: str,
    jti: str,
    token_type: TokenType,
    expires_at: int,
    parent_jti: str | None = None
):

    new_token = UserToken(

        user_id=user_id,

        jti=jti,

        parent_jti=parent_jti,

        token_type=token_type,

        expires_at=expires_at,

        is_revoked=False,

        last_used_at=int(time.time() * 1000)
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

    token.last_used_at = int(time.time() * 1000)

    db.add(token)

    db.flush()

    db.refresh(token)

    return token


# GET ACTIVE SESSIONS COUNT
def get_active_sessions_count(
    db: Session
):

    return (
        db.query(func.count(distinct(UserToken.user_id)))
        .filter(
            UserToken.is_revoked == False,
            UserToken.expires_at > int(time.time() * 1000)
        )
        .scalar()
    )

# GET ACTIVE USERS COUNT
def get_active_users_count(
    db: Session
):

    return (
        db.query(
            distinct(UserToken.user_id)
        )
        .filter(
            UserToken.is_revoked == False,
            UserToken.expires_at > int(time.time() * 1000)
        )
        .count()
    )