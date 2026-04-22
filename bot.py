import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Клавиатура
kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add("📁 Архив", "📨 Консультация")

user_state = {}

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_state[message.from_user.id] = None
    await message.answer("🗂 Добро пожаловать в систему архива", reply_markup=kb)

@dp.message_handler(lambda m: m.text == "📨 Консультация")
async def consult(message: types.Message):
    user_state[message.from_user.id] = None
    await message.answer("❗ В ближайшее время свободных окон нет")

@dp.message_handler(lambda m: m.text == "📁 Архив")
async def archive(message: types.Message):
    user_state[message.from_user.id] = "archive"
    await message.answer("🔎 Введите номер дела:")

@dp.message_handler()
async def handle(message: types.Message):
    state = user_state.get(message.from_user.id)

    if state == "archive":
        code = message.text.strip()

        if code == "071930":

            # 📁 ОТПРАВКА ФАЙЛА
            await message.answer_document(
                document="https://example.com/your_file.pdf",
                caption="📁 ДЕЛО 071930\n\nДоступ получен"
            )

        else:
            await message.answer("❌ Дело не найдено")

        user_state[message.from_user.id] = None
        return

    await message.answer("Выберите действие через меню 👇")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
