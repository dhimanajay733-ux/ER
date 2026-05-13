from sqlalchemy import create_engine, DateTime
from datetime import datetime,timezone
from sqlalchemy.orm import sessionmaker,Mapped,mapped_column,DeclarativeBase
from src.core.config import settings

# ENGINE
engine = create_engine(
    settings.db_url,
    echo=True
)

# SESSION
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# BASE CLASS
# Maps Python classes to database Tables

class Base(DeclarativeBase):

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.now(timezone.utc)
    )

# DB DEPENDENCY
def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()