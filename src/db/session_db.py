from sqlalchemy import create_engine, DateTime
#from datetime import datetime,timezone
from sqlalchemy.orm import sessionmaker,Mapped,mapped_column,DeclarativeBase
from src.core.config import settings
import time
from sqlalchemy import BigInteger

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
    pass

class TimestampMixin:

    created_at: Mapped[int] = mapped_column(
        BigInteger,
        default=lambda: int(time.time())
    )

    updated_at: Mapped[int] = mapped_column(
        BigInteger,
        default=lambda: int(time.time()),
        onupdate=lambda: int(time.time())
    )
# DB DEPENDENCY
def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()