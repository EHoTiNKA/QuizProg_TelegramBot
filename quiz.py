import json
from aiogram.enums import ParseMode
from aiogram.methods import send_poll
from aiogram.types.poll_answer import PollAnswer
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import types, Router
from aiogram.filters import Command

from models import Question


router = Router(name=__name__)

with open('questions.json', 'r') as file:
    quiz_data = json.load(file)
    questions = [Question(**question) for question in quiz_data]

class QuizState(StatesGroup):
    quiz = State()

@router.message(Command("startquiz"))
async def start_quiz(message: types.Message, state: FSMContext):

    await state.set_state(QuizState.quiz)
    await state.update_data(quiz={'question_id': 0})

    question = questions[0]

    await message.answer_poll(
        question=question.text,
        options=question.answers,
        correct_option_id=question.correct_answer_id,
        is_anonymous=False,
    )

# @router.poll_answer_handler(state=QuizState.quiz)
# async def handle_poll_answer(poll_answer: PollAnswer, state: FSMContext):
#     user_id = poll_answer.user.id
#     selected_option_id = poll_answer.option_ids[0]  # предполагаем, что только один ответ может быть выбран

#     # Ваш код для обработки ответа на опрос здесь
#     # Можете использовать state для хранения данных и следующего вопроса
#     data = await state.get_data()
#     current_question_id = data['quiz']['question_id']

#     # Проверяем, если есть следующий вопрос
#     if current_question_id + 1 < len(questions):
#         next_question_id = current_question_id + 1
#         await state.update_data(quiz={'question_id': next_question_id})
#         next_question = questions[next_question_id]

#         # Отправляем следующий вопрос
#         await poll_answer.answer_poll(
#             chat_id=user_id,
#             question=next_question.text,
#             options=next_question.answers,
#             correct_option_id=next_question.correct_answer_id,
#             is_anonymous=False,
#         )
#     else:
#         # Если вопросы закончились, завершаем состояние
#         await state.finish()
