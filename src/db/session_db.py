import time
from sqlalchemy import BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from src.core.config import settings

#  ENGINE 
engine = create_async_engine(
    settings.db_url,
    echo=True
)

#  SESSION (Switched expire_on_commit to False, which is highly recommended for async)
SessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False  
)

#  BASE CLASS
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

#  DB DEPENDENCY (Updated to be fully Asynchronous)
async def get_db():

    async with SessionLocal() as db:
        yield db