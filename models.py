from pydantic import BaseModel

class User(BaseModel):
    name: str or None = None
    group: int or None = None

class Question(BaseModel):
    text: str
    answers: list[str]
    correct_answer_id: int