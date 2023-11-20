import aiogram

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from models import User
from pony.orm import *
from db import Users, Results

API_TOKEN = "6753451845:AAHub4711K0-sbMDfC-FdvygpRlNdZLhBFk"
bot = Bot(API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

storage = MemoryStorage()
sessions = {}


class ProfileStatesGroup(StatesGroup):
    user_name = State()
    user_group = State()
    check_data = State()


@dp.message_handler(commands=["start"])  # декоратор
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


@dp.message_handler(commands=["reg"])
async def user_reg(message: types.Message):
    sessions[message.chat.id] = User()
    await bot.send_message(
        message.chat.id, "<b>Введите ваше ФИО</b>", parse_mode="html"
    )
    await ProfileStatesGroup.user_name.set()


@dp.message_handler(state=ProfileStatesGroup.user_name)
async def load_user_name(message: types.Message, state: FSMContext):
    # async with state.proxy() as data:
    #     data['user_name'] = message.text

    user = sessions[message.chat.id]
    user.name = message.text.strip()
    await bot.send_message(
        message.chat.id, "Введите вашу группу <b>(только цифры)</b>", parse_mode="html"
    )
    await ProfileStatesGroup.next()


@dp.message_handler(state=ProfileStatesGroup.user_group)
async def load_user_group(message: types.Message, state: FSMContext):
    # async with state.proxy() as data:
    #     data['user_group'] = message.text

    user = sessions[message.chat.id]
    user.group = message.text.strip()
    markup_inline = InlineKeyboardMarkup(row_width=2)
    item_yes = InlineKeyboardButton(text="Да", callback_data="yes")
    item_no = InlineKeyboardButton(text="Нет", callback_data="no")
    markup_inline.add(item_yes, item_no)
    await bot.send_message(
        message.chat.id,
        f"<b>Проверьте корректность данных:</b>\n\nВас зовут - {user.name}\nСостоите в группе - {user.group}",
        reply_markup=markup_inline,
        parse_mode="html",
    )
    await ProfileStatesGroup.next()


@dp.callback_query_handler(state=ProfileStatesGroup.check_data)
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
        await state.finish()
    elif callback.data == "no":
        # await bot.send_message(callback.message.chat.id, "Введите верные данные")
        # await bot.send_message(
        #     callback.message.chat.id,
        #     "Для прохождения регистрации введите /reg повторно!",
        # )
        await bot.send_message(
            callback.message.chat.id, "<b>Введите ваше ФИО</b>", parse_mode="html"
        )
        await state.set_state(ProfileStatesGroup.user_name)
        
    await callback.message.delete()

@dp.message_handler(commands=["startquiz"])
async def start_quiz(message: types.Message):
    pass


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
