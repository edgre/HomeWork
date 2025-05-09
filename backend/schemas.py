from typing import List
import datetime as dt
from pydantic import BaseModel

# Модель для отображения информации о пользователе
class User(BaseModel):
    username: str
    realname: str
# Модель для хранения пользователя в базе данных
class UserCreate(User):
    password: str

class UserInDB (User):
    id: int

    class Config:
        orm_mode = True

# Модель для возвращаемого токена
class Token(BaseModel):
    access_token: str
    token_type: str

class GDZCreate(BaseModel):
    description: str
    textbook_and_exercise: str
    category: str
    grade: str
    content: str
    is_elite: bool = False
