import aiogram

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from models import User
from pony.orm import *
from db import Users, Results

API_TOKEN = ('6753451845:AAHub4711K0-sbMDfC-FdvygpRlNdZLhBFk')
bot = Bot(API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

storage = MemoryStorage()
sessions = {}


class ProfileStatesGroup(StatesGroup):
    state_name = State()
    state_group = State()


@dp.message_handler(commands=['start']) #декоратор
async def start(message: types.Message):
    sessions[message.chat.id] = User()
    await bot.send_message(message.chat.id, '<b>Дооообро пожаловать на нашу викторину с вопросами про IT</b>\n\nВам предстоит пройти тест нааа 30 вопросов!\nЗа каждый правильный ответ вы получаете по 1 баллу и в конце узнаете свой результат!', parse_mode='html')
    await bot.send_message(message.chat.id, '<b>Для начала викторины зарегестрируйтесь командой /reg</b>', parse_mode='html')

@dp.message_handler(commands=['reg']) 
async def user_reg(message: types.Message):
    await bot.send_message(message.chat.id, '<b>Введите ваше ФИО</b>', parse_mode='html')
    await ProfileStatesGroup.state_name.set()

@dp.message_handler(state=ProfileStatesGroup.state_name)
async def load_state_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['state_name'] = message.text

    user = sessions[message.chat.id]
    user.name = message.text.strip()
    await bot.send_message(message.chat.id, 'Введите вашу группу <b>(только цифры)</b>', parse_mode='html')
    await ProfileStatesGroup.next()

@dp.message_handler(state=ProfileStatesGroup.state_group)
async def load_state_group(message: types.Message, state:FSMContext):
    # user = sessions[message.chat.id]
    # user.group = message.text.strip()
    async with state.proxy() as data:
        data['state_group'] = message.text

    await bot.send_message(message.chat.id, '<b>Данные сохранены!</b>', parse_mode='html')
    await state.finish()

async def user_reg_confirm(message):
    user = sessions[message.chat.id]
    user.group = message.text.strip()
    markup_inline = InlineKeyboardMarkup(row_width=2)
    item_yes = InlineKeyboardButton(text = 'Да', callback_data = 'yes')
    item_no = InlineKeyboardButton(text = 'Нет', callback_data = 'no')
    markup_inline.add(item_yes, item_no)
    await bot.send_message(message.chat.id, f'<b>Проверьте корректность данных:</b>\n\nВас зовут - {user.name}\nСостоите в группе - {user.group}', reply_markup=markup_inline, parse_mode='html')




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


