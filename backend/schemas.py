from typing import List
import datetime as dt
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, Union
import base64

class User(BaseModel):
    username: str
    realname: str


class UserCreate(User):
    password: str

class UserInDB (User):
    id: int
    class Config:
        from_attributes = True

# Модель для возвращаемого токена
class Token(BaseModel):
    access_token: str
    token_type: str

class GDZCreate(BaseModel):
        description: str
        textbook: str
        exercise: str
        subject: str
        category: str
        price: int
        rating: float = 0.0
        is_elite: bool = False
        content_text: str

        model_config = ConfigDict(from_attributes=True)

class GDZPublic(BaseModel):
    id: int
    owner_id: int
    description: str
    textbook: str
    exercise: str
    subject: str
    price: int
    category: str
    rating: float
    is_elite: bool

class GDZPrivate(GDZPublic):
    content: str

class GDZRatingIn(BaseModel):
    gdz_id: int
    value: int  # от 1 до 5