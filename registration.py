from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from pony.orm import *

from db import Users
from models import User

router = Router(name=__name__)

sessions = {}


class ProfileStatesGroup(StatesGroup):
    user_name = State()
    user_group = State()
    check_data = State()

@router.message(Command("reg"))
async def user_reg(message: types.Message, state: FSMContext):
    sessions[message.chat.id] = User()
    await message.answer(
        "<b>Введите ваше ФИО</b>", parse_mode="html"
    )
    await state.set_state(ProfileStatesGroup.user_name)


@router.message(ProfileStatesGroup.user_name)
async def load_user_name(message: types.Message, state: FSMContext):
    user = sessions[message.chat.id]
    user.name = message.text.strip()
    await message.answer(
        "Введите вашу группу <b>(только цифры)</b>", parse_mode="html"
    )
    await state.set_state(ProfileStatesGroup.user_group)


@router.message(ProfileStatesGroup.user_group)
async def load_user_group(message: types.Message, state: FSMContext):
    user = sessions[message.chat.id]
    user.group = message.text.strip()
    builder = InlineKeyboardBuilder()
    builder.button(text="Да", callback_data="yes")
    builder.button(text="Нет", callback_data="no")
    await message.answer(
        
        f"<b>Проверьте корректность данных:</b>\n\nВас зовут - {user.name}\nСостоите в группе - {user.group}",
        reply_markup=builder.as_markup(),
        parse_mode="html",
    )
    await state.set_state(ProfileStatesGroup.check_data)


@router.callback_query(ProfileStatesGroup.check_data)
async def callback_analysis(callback: types.CallbackQuery, state: FSMContext):
    user = sessions[callback.message.chat.id]
    if callback.data == "yes":

        @db_session
        def add_user():
            Users(name=f"{user.name}", group=f"{user.group}")

        add_user()
        commit()
        await callback.message.answer(
            
            "<b>Данные успешно сохранены!</b>",
            parse_mode="html",
        )
        await callback.message.answer(
            
            "Отлично теперь вы можете начать тест\nЭто тест на знания в сфере IT из 30ти вопросов\nЧтобы начать тест введите /startquiz",
        )

    elif callback.data == "no":
        await callback.message.answer(
            "<b>Введите ваше ФИО</b>", parse_mode="html"
        )
        await state.set_state(ProfileStatesGroup.user_name)

    await callback.message.delete()
