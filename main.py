import asyncio
import logging
import sys
import database.requests as rq
import aiogram.utils.markdown as fmt

from os import getenv
from dotenv import load_dotenv
from group_work.user_work import user_router
from loader import bot
from aiogram import Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from database.models import async_main

load_dotenv()
# Bot token can be obtained via https://t.me/BotFather
TOKEN = getenv("BOT_TOKEN")
print(TOKEN)

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()

@dp.message(CommandStart())
async def echo(message: types.Message):
    user_id = message.from_user.id
    chat_id = int(getenv("CHAT_ID"))
    await rq.set_user(message.from_user.id,
                      message.from_user.username,
                      message.from_user.first_name,
                      message.from_user.last_name)
    await message.answer(
        fmt.text(
            fmt.text("📣", fmt.hbold("ВАЖНАЯ ИНФОРМАЦИЯ")),
            fmt.text(""),
            fmt.text(
                "Размещайте объявления о потерянных и найденных "
                "вещах БЕСПЛАТНО в нашей <a href='https://t.me/gdenaiti_metro'>telegram</a> группе и странице в <a href='https://vk.com/buro_mm'>VK</a>"),
            fmt.text(""),
            fmt.text(fmt.hbold("ВНИМАНИЕ!")),
            fmt.text("- Остерегайтесь мошенников!"),
            fmt.text("- Требуйте описания найденных предметов!"),
            fmt.text("- Никогда не переводите деньги заранее!"),
            fmt.text("- Вознаграждение передавайте ТОЛЬКО при личной встрече!"),
            fmt.text("- Вознаграждение передавайте ТОЛЬКО при личной встрече!"),
            sep="\n"
        ), parse_mode="HTML", disable_web_page_preview=True,
    )
    await message.answer(
        fmt.text(
            fmt.text("Вы успешно подписались! Доступ к чату открыт"),
            fmt.text("Нажмите на <a href='https://t.me/gdenaiti_metro'>cсылку</a>, чтобы вернуться назад в чат"),
            sep="\n"
        ), parse_mode="HTML"
    )


# @dp.message(Command("help"))
# async def help(message: types.Message):
#     await message.answer("Раздел в разработке")
@dp.message(Command("help"))
async def help(message: types.Message):
    await message.answer(
        "Что делать, если вы оставили вещь в метро, МЦК, МЦД или в наземном транспорте?\n\n"
        "Можете обратиться к нам любым удобным для вас способом:\n\n"
        "🔹 по номеру 3210 с мобильного телефона\n"
        "🔹 через чат-бот Александра: https://t.me/transport_mos_bot\n"
        "🔹 создать обращение о потере вещей в приложении «Метро Москвы»: https://www.mosmetro.ru/app/\n\n"
        "Наши склады есть на станциях:\n\n"
        "1️⃣ «Черкизовская» — последний вагон из центра, выход 1\n"
        "7️⃣ «Котельники» — восточный вестибюль — первый вагон из центра\n"
        "1️⃣ «Деловой центр» — второй ярус станции, помещение 1077\n\n"
        "Режим работы Складов забытых вещей: каждый день с 8:00 до 20:00\n"
        "Подробнее: https://mosmetro.ru/passengers/services/lost-and-found/\n\n"
        "Информация взята с сайта: https://transport.mos.ru/mostrans/all_news/113951"
    )	

@dp.message(F.new_chat_members)
async def mes_new_user(message: types.Message):
    await message.delete()

@dp.message(F.left_chat_member)
async def mes_left_user(message: types.Message):
    await message.delete()
    
async def main() -> None:
    await async_main()
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    dp.include_routers(user_router)
    # And the run events dispatching
    await dp.start_polling(bot, allowed_updates=["message", "chat_member"])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")