import json
from aiogram.enums import ParseMode
from aiogram.methods import send_poll
from aiogram.types.poll_answer import PollAnswer
from aiogram import types, Router
from aiogram.filters import Command


router = Router(name=__name__)


@router.message(Command("startquiz"))
async def start_quiz(message: types.Message):
    with open('questions.json', 'r') as file:
        questions = json.load(file)

    await router.send_poll(
        chat_id=message.chat.id,
        question="Сколько будет 2 + 2",
        options=["3", "4", "1"],
        correct_option_id=1,
        is_anonymous=False,
    )