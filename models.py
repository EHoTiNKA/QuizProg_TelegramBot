from pydantic import BaseModel

class User(BaseModel):
    name: str or None = None
    group: int or None = None