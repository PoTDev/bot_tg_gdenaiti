from data.permissions import new_user_added
from aiogram import Router, types, F, Bot
from os import getenv
from dotenv import load_dotenv
import aiogram.utils.markdown as fmt
from aiogram.utils.keyboard import InlineKeyboardBuilder
import database.requests as rq
from loader import bot

load_dotenv()

CHAT_ID = getenv("CHAT_ID")
TOKEN = getenv("BOT_TOKEN")
user_router = Router()
@user_router.message(F.chat.id == int(CHAT_ID))
async def mes(message: types.Message):
     print(message.from_user.id)
     is_user_exist = await rq.check_user(message.from_user.id)
     if not is_user_exist:
          await bot.restrict_chat_member(
               chat_id=message.chat.id,
               user_id=message.from_user.id,
               permissions=new_user_added,
          )
          # Написать что нужно подписаться на бота
          builder = InlineKeyboardBuilder()
          builder.row(types.InlineKeyboardButton(
               text="Подписаться на бота", url="tg://resolve?domain=GdenaitiBot"))
          await message.answer(
               fmt.text(fmt.hbold(message.from_user.full_name),
                    fmt.text(", вы находитесь в режиме чтения. "
                             "Чтобы писать в чате, пожалуйста, подпишитесь на бота, нажав на кнопку ниже"),
                    sep=""
               ), parse_mode="HTML", reply_markup=builder.as_markup(),
          )

