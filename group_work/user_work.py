# group_work/user_work.py
import asyncio
from aiogram import Router, types, Bot
from aiogram.types import ChatMemberUpdated
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, JOIN_TRANSITION
from aiogram.utils.markdown import hbold, text
from aiogram.utils.keyboard import InlineKeyboardBuilder
from data.permissions import new_user_added
from loader import bot
from os import getenv
from dotenv import load_dotenv

load_dotenv()
CHAT_ID = int(getenv("CHAT_ID"))

user_router = Router()

@user_router.chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION))
async def on_user_joined(event: ChatMemberUpdated, bot: Bot):
    user = event.from_user
    chat_id = event.chat.id

    # Ограничиваем пользователя
    await bot.restrict_chat_member(
        chat_id=chat_id,
        user_id=user.id,
        permissions=new_user_added
    )

    # Сообщение с кнопкой подписки
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Подписаться на бота", url="tg://resolve?domain=GdenaitiBot"
    ))

    try:
        msg = await bot.send_message(
            chat_id=chat_id,
            text=text(
                hbold(user.full_name),
                ", вы находитесь в режиме чтения. "
                "Чтобы писать в чате, подпишитесь на бота, нажав на кнопку ниже."
            ),
            parse_mode="HTML",
            reply_markup=builder.as_markup()
        )
        await asyncio.sleep(60)
        await msg.delete()
    except Exception:
        pass