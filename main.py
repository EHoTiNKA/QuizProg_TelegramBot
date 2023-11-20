import aiogram
import logging
import sys
import asyncio
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from models import User
from pony.orm import *
from db import Users, Results

API_TOKEN = "6753451845:AAHub4711K0-sbMDfC-FdvygpRlNdZLhBFk"
bot = Bot(API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()


sessions = {}


class ProfileStatesGroup(StatesGroup):
    user_name = State()
    user_group = State()
    check_data = State()


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


@dp.message(Command('reg'))
async def user_reg(message: types.Message, state: FSMContext):
    sessions[message.chat.id] = User()
    await bot.send_message(
        message.chat.id, "<b>Введите ваше ФИО</b>", parse_mode="html"
    )
    await state.set_state(ProfileStatesGroup.user_name)


@dp.message(ProfileStatesGroup.user_name)
async def load_user_name(message: types.Message, state: FSMContext):
    user = sessions[message.chat.id]
    user.name = message.text.strip()
    await bot.send_message(
        message.chat.id, "Введите вашу группу <b>(только цифры)</b>", parse_mode="html"
    )
    await state.set_state(ProfileStatesGroup.user_group)


@dp.message(ProfileStatesGroup.user_group)
async def load_user_group(message: types.Message, state: FSMContext):
    user = sessions[message.chat.id]
    user.group = message.text.strip()
    builder = InlineKeyboardBuilder()
    builder.button(text='Да', callback_data='yes')
    builder.button(text='Нет', callback_data='no')
    await bot.send_message(
        message.chat.id,
        f"<b>Проверьте корректность данных:</b>\n\nВас зовут - {user.name}\nСостоите в группе - {user.group}",
        reply_markup=builder.as_markup(),
        parse_mode="html",
    )
    await state.set_state(ProfileStatesGroup.check_data)
    


@dp.callback_query(ProfileStatesGroup.check_data)
async def callback_analysis(callback: types.CallbackQuery, state: FSMContext):
    user = sessions[callback.message.chat.id]
    if callback.data == "yes":

        @db_session
        def add_user():
            Users(name=f"{user.name}", group=f"{user.group}")

        add_user()
        commit()
        await bot.send_message(
            callback.message.chat.id,
            "<b>Данные успешно сохранены!</b>",
            parse_mode="html",
        )
        await bot.send_message(
            callback.message.chat.id,
            "Отлично теперь вы можете начать тест\nЭто тест на знания в сфере IT из 30ти вопросов\nЧтобы начать тест введите /startquiz",
        )
        
    elif callback.data == "no":
        await bot.send_message(
            callback.message.chat.id, "<b>Введите ваше ФИО</b>", parse_mode="html"
        )
        await state.set_state(ProfileStatesGroup.user_name)
        
    await callback.message.delete()

@dp.message(Command('startquiz'))
async def start_quiz(message: types.Message):
    pass

async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
