import logging
import sys
import asyncio

from aiogram import Dispatcher, types
from aiogram.filters import CommandStart

from bot import bot
import registration, quiz


dp = Dispatcher()
dp.include_router(registration.router)
dp.include_router(quiz.router)



@dp.message(CommandStart())  # декоратор
async def start(message: types.Message):
    await bot.send_message(
        message.chat.id,
        "<b>Дооообро пожаловать на нашу викторину с вопросами про IT</b>\n\nВам предстоит пройти тест нааа 30 вопросов!\nЗа каждый правильный ответ вы получаете по 1 баллу и в конце узнаете свой результат!",
        parse_mode="html",
    )
    await bot.send_message(
        message.chat.id,
        "<b>Для начала викторины зарегестрируйтесь командой /reg</b>",
        parse_mode="html",
    )




async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
