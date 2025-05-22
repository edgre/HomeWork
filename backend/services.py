import os
from fastapi import FastAPI, HTTPException, Depends, UploadFile
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy import select
from uuid import uuid4
import aiofiles
import jwt
from datetime import datetime, timedelta
import sqlalchemy.orm as orm
import models
import schemas
import database as _db
from schemas import User, UserInDB, Token
from pathlib import Path

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

async def authenticate_user(db: orm.Session, username: str, password: str):
    user = await get_user(db, username)
    if (not user) or (not await verify_password(password, user.password_hash)):
        return False
    return user

async def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def create_access_token(user: models.User, expires_delta: timedelta | None = None):
    user_obj = schemas.UserInDB.from_orm(user)
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    payload = user_obj.dict()
    payload["exp"] = expire
    token = jwt.encode(payload, SECRET_KEY)
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return {"access_token": token}

async def get_current_user(
    db: orm.Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        print(payload)
        user = db.query(models.User).get(payload["id"])
    except:
        raise HTTPException(
            status_code=401, detail="Invalid JWT token")
    return schemas.UserInDB.from_orm(user)

async def get_user (db: orm.Session(), username: str):
   return db.query(models.User).filter(models.User.username == username).first()


async def create_user(db: orm.Session(), user: schemas.UserCreate):
    user_obj = models.User(
        realname=user.realname,
        username=user.username,
        password_hash=get_password_hash(user.password)
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


async def save_uploaded_file(file: UploadFile, upload_dir: str = "media") -> str:
    Path(upload_dir).mkdir(parents=True, exist_ok=True)
    # Получаем оригинальное расширение файла или используем .png по умолчанию
    file_ext = file.filename.split('.')[-1] if '.' in file.filename else 'png'
    if file_ext in ['png', 'jpg', 'jpeg', 'webp']:  # Можно расширить список допустимых форматов

        filename = f"{uuid4()}.{file_ext}"
        filepath = os.path.join(upload_dir, filename)

        # Асинхронно сохраняем файл
        try:
            async with aiofiles.open(filepath, "wb") as buffer:
                while chunk := await file.read(1024 * 1024):  # Читаем по 1MB за раз
                    await buffer.write(chunk)
        except Exception as e:
            raise HTTPException(500, detail=f"Ошибка при сохранении файла: {str(e)}")
        path = f'images/{filename}'
        print(path)
        return path

async def get_image(
    name: str
):
    print(name)
    return FileResponse(f"media/{name}", headers={"Cache-Control": "no-cache"})


async def create_gdz(
        db: orm.Session,
        gdz_data: schemas.GDZCreate,
        file_content: UploadFile,
        owner_id: str
):
    try:
        # Сохраняем файл
        filename = await save_uploaded_file(file_content)

        # Создаем запись в БД
        gdz = models.GDZ(
            description=gdz_data.description,
            full_description=gdz_data.full_description,
            category=gdz_data.category,
            owner_id=owner_id,
            content=filename,
            content_text=gdz_data.content_text,
            price=gdz_data.price
        )

        db.add(gdz)
        db.commit()
        db.refresh(gdz)
        return gdz

    except HTTPException:
        raise  # Пробрасываем уже обработанные ошибки
    except Exception as e:
        db.rollback()
        raise HTTPException(500, detail=f"Ошибка при создании записи: {str(e)}")


async def get_gdz_by_id(
        db: orm.Session,
        gdz_id: int):
    return db.query(models.GDZ).filter(models.GDZ.id == gdz_id).first()


async def get_all_gdz_sorted_by_rating(db: orm.Session, descending: bool = True):
    stmt = select(models.GDZ).where(models.GDZ.rating.is_not(None))

    if descending:
        stmt = stmt.order_by(models.GDZ.rating.desc())
    else:
        stmt = stmt.order_by(models.GDZ.rating.asc())

    result = await db.execute(stmt)
    return result.scalars().all()


async def get_gdz_by_owner(db: orm.Session, user_id: int):
    return db.query(models.GDZ).filter(models.GDZ.owner_id == user_id).all()

async def is_gdz_free(db: orm.Session, gdz_id: int):
    gdz = await get_gdz_by_id(db, gdz_id)
    return gdz and gdz.price == 0


async def get_user_purchases(db: orm.Session, user_id: int):
    stmt = (
        select(models.GDZ)  # Выбираем GDZ, а не Purchase
        .join(models.Purchase, models.Purchase.gdz_id == models.GDZ.id)  # Соединяем с Purchase
        .where(models.Purchase.buyer_id == user_id)  # Только покупки текущего пользователя
    )
    result = db.execute(stmt)
    return result.scalars().all()  # Возвращаем GDZ, а не Purchase


async def get_purchase(db: orm.Session, user_id: int, gdz_id: int):
    """Проверяет, есть ли покупка указанного ГДЗ у пользователя"""
    stmt = (
        select(models.Purchase)
        .where(models.Purchase.buyer_id == user_id)
        .where(models.Purchase.gdz_id == gdz_id)
    )
    result = db.execute(stmt)
    return result.scalar_one_or_none()


async def validate_signature(
        db: orm.Session,
        user_id: int,
        gdz_id: int,
        signature: int,
):
    n = 976244680564357686203172406534020527158624852187877139888568277444800468497409358863572759
    e = 3
    code = db.execute(
        select(models.Codes.code)
        .where(models.Codes.user_id == user_id)
        .where(models.Codes.gdz_id == gdz_id)
    ).scalar()

    decrypted = pow(signature, e, n)
    print(decrypted, code)
    return decrypted == code


def update_user_rating(db: orm.Session, owner_id: int):
    """Обновляет рейтинг пользователя на основе его ГДЗ"""
    user = db.query(models.User).get(owner_id)
    if not user:
        return

    # Находим все оценки всех ГДЗ пользователя через связь
    ratings = (
        db.query(models.GDZRating.value)
        .join(models.GDZ)
        .filter(models.GDZ.owner_id == owner_id)
        .all()
    )

    if ratings:
        avg_rating = sum(r[0] for r in ratings) / len(ratings)
        user.user_rating = round(avg_rating, 2)
    else:
        user.user_rating = 0.0

    db.commit()
