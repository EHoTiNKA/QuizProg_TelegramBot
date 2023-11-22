import json
import logging
import sys
import asyncio
from aiogram.enums import ParseMode
from aiogram.methods import send_poll
from aiogram.types.poll_answer import PollAnswer
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command

import registration, quiz

API_TOKEN = "6753451845:AAHub4711K0-sbMDfC-FdvygpRlNdZLhBFk"
bot = Bot(API_TOKEN, parse_mode=ParseMode.HTML)
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
