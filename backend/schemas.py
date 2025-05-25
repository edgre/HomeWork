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
    user_rating: float = 0.0
    has_draft: bool
    class Config:
        from_attributes = True

# Модель для возвращаемого токена
class Token(BaseModel):
    access_token: str
    token_type: str

class GDZCreate(BaseModel):
        description: str
        full_description: str
        category: str
        price: int
        # rating: float = 0.0s
        is_elite: bool = False
        content_text: str

        model_config = ConfigDict(from_attributes=True)

class GDZPublicShort(BaseModel):
    id:int
    owner_id: int
    price:int
    description:str
    has_purchased: bool
    is_elite: bool

class GDZPublic(BaseModel):
    id: int
    owner_id: int
    description: str
    price: int
    category: str
    is_elite: bool

class GDZPrivate(GDZPublic):
    content: str
    full_description: str
    content_text: str

class GDZRatingIn(BaseModel):
    gdz_id: int
    value: int  # от 1 до

class UserProfileResponse(BaseModel):
    username: str
    realname: str
    user_rating: Optional[float] = None
    # is_elite: bool
    gdz_list: List[GDZPublic]  # Используем существующую модель GDZPrivate

    class Config:
        from_attributes = True


class Signature(BaseModel):
    value: int

class DraftData(BaseModel):
    description: Optional[str] = None
    full_description: Optional[str] = None
    category: Optional[str] = None
    subject: Optional[str] = None
    content_text: Optional[str] = None
    price: Optional[float] = None
    is_elite: Optional[bool] = None
    gdz_id: Optional[int] = None

class DraftResponse(BaseModel):
    draft_id: int
    file_path: str