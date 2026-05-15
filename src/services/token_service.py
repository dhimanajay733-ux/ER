from sqlalchemy.orm import Session

from src.repository.token_repository import (
    get_active_sessions_count,
    get_active_users_count
)


def active_sessions(
    db: Session
):

    return get_active_sessions_count(db)


def active_users(
    db: Session
):

    return get_active_users_count(db)