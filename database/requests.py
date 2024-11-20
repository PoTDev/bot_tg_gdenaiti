from sqlalchemy.ext.asyncio import AsyncSession

from database.models import async_session
from database.models import User
from sqlalchemy import select, update, Column, TIMESTAMP, text
from datetime import datetime

async def set_user(user_id: int, username: str, first_name: str, last_name: str) -> bool:
    async with async_session() as session:
        is_exists = await session.scalar(select(User).where(User.user_id == user_id))
        await change_active(session, user_id)
        if not is_exists:
            session.add(User(user_id=user_id, username=username, first_name=first_name, last_name=last_name))
            await session.commit()
            return False


async def check_user(user_id: int):
    async with async_session() as session:
        user_is_exist = await session.scalar(select(User).where(User.user_id == user_id))
        if user_is_exist:
            await change_active(session, user_id)
            return True
        else:
            return False


async def change_active(session: AsyncSession, user_id: int) -> None:
    await session.execute(update(User).filter(User.user_id == user_id).values(last_activity=datetime.now()))
    await session.commit()