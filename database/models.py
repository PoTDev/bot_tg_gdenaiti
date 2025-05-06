from sqlalchemy import BigInteger, String, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.sql import func
from os import getenv
from dotenv import load_dotenv
load_dotenv()


DATABASE_URL = getenv("DATABASE_URL")


engine = create_async_engine(url=DATABASE_URL)

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(BigInteger)
    username: Mapped[str] = mapped_column(String(32), nullable=True)
    first_name: Mapped[str] = mapped_column(String(64), nullable=True)
    last_name: Mapped[str] = mapped_column(String(64), nullable=True)
    last_activity = mapped_column(DateTime(timezone=True), default=func.now())


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)