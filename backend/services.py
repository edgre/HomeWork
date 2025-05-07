import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import sqlalchemy.orm as orm
import models
import schemas
import database as _db

from schemas import User, UserInDB, Token

app = FastAPI()
SECRET_KEY = os.environ.get("JWT_SECRET_KEY", os.urandom(32).hex())
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

async def add_to_db(db: orm.Session(), class_obj):
    db.add(class_obj)
    db.commit()
    db.refresh(class_obj)

def get_db():
    db = _db.Session()
    try:
        yield db
    finally:
        db.close()

def get_password_hash(password):
    return pwd_context.hash(password)

async def get_user (db: orm.Session(), username: str):
   return db.query(models.User).filter(models.User.username == username).first()

async def create_user(db: orm.Session(), user: schemas.UserCreate):
        user_obj = models.User(
            username=user.username,
            realname=user.realname,
            password_hash=get_password_hash(user.password)
        )
        db.add(user_obj)
        db.commit()
        db.refresh(user_obj)
        return user_obj

async def authenticate_user(db: orm.Session, username: str, password: str):
    user = await get_user(db, username)
    if (not user) or (not verify_password(password, user.hashed_password)):
        return False
    return user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


