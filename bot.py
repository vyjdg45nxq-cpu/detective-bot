import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

# ====== НАСТРОЙКИ ======
TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

# ====== "БАЗА ДЕЛ" (пока внутри кода) ======
cases = {
    "101": {
        "title": "Дело №101",
        "name": "Иван Петров",
        "status": "Подозреваемый",
        "info": "Мошенничество в особо крупном размере"
    },
    "102": {
        "title": "Дело №102",
        "name": "Анна Смирнова",
        "status": "Свидетель",
        "info": "Проходит по делу о краже документов"
    },
    "000": {
        "title": "ДОСТУП ОГРАНИЧЕН",
        "name": "—",
        "status": "—",
        "info": "Файл повреждён или засекречен"
    }
}

# ====== КЛАВИАТУРА ======
kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(
    KeyboardButton("📁 Архив"),
    KeyboardButton("📨 Обращение")
)

user_state = {}

# ====== START ======
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_state[message.from_user.id] = None
    await message.answer(
        "🗂 Добро пожаловать в архив расследований",
        reply_markup=kb
    )

# ====== АРХИВ ======
@dp.message_handler(lambda message: message.text == "📁 Архив")
async def archive(message: types.Message):
    user_state[message.from_user.id] = "archive"
    await message.answer("🔎 Введите номер дела:")

# ====== ОБРАЩЕНИЕ ======
@dp.message_handler(lambda message: message.text == "📨 Обращение")
async def contact(message: types.Message):
    user_state[message.from_user.id] = "contact"
    await message.answer("✉ Напишите ваше сообщение для администратора:")

# ====== ОБРАБОТКА ВВОДА ======
@dp.message_handler()
async def handle_message(message: types.Message):
    state = user_state.get(message.from_user.id)

    # --- Архив ---
    if state == "archive":
        code = message.text.strip()

        case = cases.get(code)

        if case:
            await message.answer(
                f"{case['title']}\n\n"
                f"👤 Имя: {case['name']}\n"
                f"📌 Статус: {case['status']}\n"
                f"📂 Информация: {case['info']}"
            )
        else:
            await message.answer("❌ Дело не найдено")

        user_state[message.from_user.id] = None
        return

    # --- Обращение ---
    if state == "contact":
        ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

        if ADMIN_ID:
            await bot.send_message(
                ADMIN_ID,
                f"📨 Новое сообщение:\n\n"
                f"От: {message.from_user.id}\n"
                f"Текст: {message.text}"
            )

        await message.answer("✅ Сообщение отправлено в архив")
        user_state[message.from_user.id] = None
        return

    await message.answer("Выберите действие через меню 👇")


# ====== ЗАПУСК ======
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
