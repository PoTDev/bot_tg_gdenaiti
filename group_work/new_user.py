from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.enums.chat_type import ChatType
from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER, ChatMemberUpdatedFilter
from os import getenv
from dotenv import load_dotenv
from pyexpat.errors import messages

import database.requests as rq
load_dotenv()

CHAT_ID = getenv("CHAT_ID")

user_router = Router()
# user_router.chat_member.filter(F.chat.id == CHAT_ID)

# @user_router.message()
# async def what(message: types.Message):
#      print(message.chat.id)

# @user_router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
# async def what_is(message: types.ChatMemberUpdated):
#      for i in message:
#           print(i)
@user_router.message(F.chat.id == int(CHAT_ID))
async def mes(message: types.Message):
     print(message.from_user.id)
     is_user_exist = await rq.check_user(message.from_user.id)
     if is_user_exist:
          await message.answer(text="TRUE")
     else:
          await message.answer(text="FALSE")

     # if message.chat.id == int(CHAT_ID):
     #      for i in message:
     #           print(i)
     #      await message.answer(text="TRUE")
     # else:
     #      await message.answer(text="FALSE")

