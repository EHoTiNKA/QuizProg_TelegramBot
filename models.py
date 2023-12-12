from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str or None = None
    group: str or None = None

class Question(BaseModel):
    text: str
    answers: list[str]
    correct_answer_id: int