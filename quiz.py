import json

from aiogram.types.poll_answer import PollAnswer
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import types, Router
from aiogram.filters import Command

from models import Question
from bot import bot


router = Router(name=__name__)

with open("questions.json", "r") as file:
    quiz_data = json.load(file)
    questions = [Question(**question) for question in quiz_data]


class QuizState(StatesGroup):
    quiz = State()


@router.message(Command("startquiz"))
async def start_quiz(message: types.Message, state: FSMContext):
    await state.set_state(QuizState.quiz)
    await state.update_data(quiz={"question_id": 0})

    question = questions[0]

    await message.answer_poll(
        question=question.text,
        options=question.answers,
        correct_option_id=question.correct_answer_id,
        is_anonymous=False,
    )


@router.poll_answer(QuizState.quiz)
async def poll_answer(poll_answer: PollAnswer, state: FSMContext):
    question_id = (await state.get_data()).get("quiz").get("question_id")

    # Increment the question number
    question_id += 1

    # Check if there are more questions
    if question_id < len(questions):
        # Update the state with the new question number
        await state.update_data(quiz={"question_id": question_id})

        # Get the next question
        next_question = questions[question_id]

        # Send the next poll
        await bot.send_poll(
            chat_id=poll_answer.user.id,
            question=next_question.text,
            options=next_question.answers,
            correct_option_id=next_question.correct_answer_id,
            is_anonymous=False,
        )
    else:
        # No more questions, end the quiz
        await state.clear()
        await bot.send_message(poll_answer.user.id, "Quiz completed!")
