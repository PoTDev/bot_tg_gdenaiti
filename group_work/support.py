from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dotenv import load_dotenv
from os import getenv

router = Router()
load_dotenv()
ADMIN_CHAT_ID = getenv("ADMIN_CHAT_ID")  # Замените на ID администратора

class SupportStates(StatesGroup):
    waiting_for_question = State()

# Команда /support
@router.message(Command("support"))
async def support_start(message: Message, state: FSMContext):
    await message.answer("✉️ Напишите ваш вопрос, и мы постараемся ответить.")
    await state.set_state(SupportStates.waiting_for_question)

# Получение вопроса и пересылка админу
@router.message(SupportStates.waiting_for_question)
async def receive_question(message: Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    username = message.from_user.username or "Без username"

    # Сохраняем user_id в начало сообщения для парсинга
    text_to_admin = (
        f"[USER_ID:{user_id}]\n"
        f"📩 Вопрос от @{username}:\n\n"
        f"{message.text}"
    )

    await message.bot.send_message(ADMIN_CHAT_ID, text_to_admin)
    await message.answer("✅ Ваш вопрос отправлен. Ожидайте ответа.")

# Ответ администратора на сообщение в reply
@router.message(F.reply_to_message)
async def admin_reply(message: Message):
    reply_text = message.reply_to_message.text
    if "[USER_ID:" not in reply_text:
        return  # Это не support-вопрос

    try:
        user_id = int(reply_text.split("[USER_ID:")[1].split("]")[0])
        await message.bot.send_message(user_id, f"📬 Ответ от администрации:\n\n{message.text}")
        await message.answer("✅ Ответ отправлен пользователю.")
    except Exception as e:
        await message.answer("❌ Не удалось отправить. Проверьте формат.")