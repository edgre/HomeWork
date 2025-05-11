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

class GDZBase(BaseModel):
        """Базовая схема для GDZ (без файлового контента)"""
        description: str
        textbook: str
        exercise: str
        subject: str
        category: str
        rating: int
        is_elite: bool = False

        model_config = ConfigDict(from_attributes=True)

class GDZPublic(GDZBase):
    id: int
    owner_id: str
    rating: int = 0

class GDZPrivate(GDZPublic):
    content_file: str



