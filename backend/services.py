import os
from fastapi import FastAPI, HTTPException, Depends, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from uuid import uuid4
import aiofiles
import jwt
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


async def get_user(db: orm.Session(), username: str):
    return db.query(models.User).filter(models.User.username == username).first()


async def authenticate_user(db: orm.Session, username: str, password: str):
    user = await get_user(db, username)
    if (not user) or (not verify_password(password, user.password_hash)):
        return False
    return user


async def get_current_user(
    db: orm.Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        print(payload)
        user = db.query(models.User).get(payload["id"])
    except:
        raise HTTPException(status_code=401, detail="Invalid JWT token")
    return schemas.UserInDB.from_orm(user)


async def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def create_access_token(
    user: models.User, expires_delta: timedelta | None = None
):
    user_obj = schemas.UserInDB.from_orm(user)
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    payload = user_obj.dict()
    payload["exp"] = expire
    token = jwt.encode(payload, SECRET_KEY)
    return {"access_token": token}


async def create_user(db: orm.Session(), user: schemas.UserCreate):
    user_obj = models.User(
        realname=user.realname,
        username=user.username,
        password_hash=get_password_hash(user.password),
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


async def create_gdz(
    db: orm.Session, gdz_data: schemas.GDZBase, file_content: UploadFile, owner_id: str
):
    # Создаем папку media если ее нет

    try:
        # Генерируем уникальное имя файла
        file_ext = "png"
        filename = f"{uuid4()}.{file_ext}"

        filename = str(uuid4())
        while db.query(models.GDZ).filter_by(content=filename).first() != None:
            filename = str(uuid4())

        filepath = f"media{filename}"

        # Асинхронно сохраняем файл
        async with aiofiles.open(filepath, "wb") as buffer:
            while chunk := await file_content.read(1024 * 1024):  # Читаем по 1MB
                await buffer.write(chunk)

        # Создаем запись в БД
        gdz = models.GDZ(
            description=gdz_data.description,
            textbook=gdz_data.textbook,
            exercise=gdz_data.exercise,
            subject=gdz_data.subject,
            category=gdz_data.category,
            is_elite=gdz_data.is_elite,
            owner_id=owner_id,
            content=filename,
        )

        db.add(gdz)
        db.commit()
        db.refresh(gdz)
        return gdz

    except Exception as e:
        raise HTTPException(500, detail=f"Ошибка при сохранении: {str(e)}")


async def get_gdz_by_id(db: orm.Session, gdz_id: int):
    return db.query(models.GDZ).filter(models.GDZ.id == gdz_id).first()


async def get_all_gdz_sorted_by_rating(db: orm.Session, descending: bool = True):
    order = models.GDZ.rating.desc() if descending else models.GDZ.rating.asc()
    return db.query(models.GDZ).order_by(order).all()


async def get_gdz_by_owner(db: orm.Session, user_id: int):
    return db.query(models.GDZ).filter(models.GDZ.id == user_id).all()
