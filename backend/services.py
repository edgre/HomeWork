import os
import re
import secrets
from fastapi import FastAPI, HTTPException, Depends, UploadFile, Body
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy import or_
import sqlalchemy.orm as orm
from uuid import uuid4
import aiofiles
import jwt
from datetime import datetime, timedelta
from Crypto.Util.number import bytes_to_long, long_to_bytes
from cryptohash import sha1
from pathlib import Path
from typing import List, Dict, Any, Optional
from jinja2 import Environment
import json
import asyncio
import database as _db
import models
import schemas

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

async def get_profile_data(db: orm.session, user:schemas.UserInDB):
    user = db.query(models.User).filter(models.User.id == user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_user_rating(db, user.id)

    created_gdz = db.query(models.GDZ).filter(models.GDZ.owner_id == user.id).all()
    gdz_list = []

    for gdz in created_gdz:
        gdz_list.append({
            "id": gdz.id,
            "description": gdz.description,
            "category": gdz.category,
            "content": gdz.content,
            "content_text": gdz.content_text,
            "price": gdz.price,
            "is_elite": gdz.is_elite,
            "owner_id": gdz.owner_id == user.id

        })

    return {
        "username": user.username,
        "realname": user.realname,
        "user_rating": user.user_rating,
        # "is_elite": user.is_elite,
        "gdz_list": gdz_list
    }


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


async def get_subjects_by_category(db: orm.Session(), category: str):
    subjects = db.query(
        models.Subjects.subject_name,
        models.Subjects.paths
    ).filter(
        models.Subjects.category == category
    ).all()
    return [ subject.subject_name for subject in subjects]


async def save_uploaded_file(file: UploadFile, upload_dir: str = "media") -> str:
    Path(upload_dir).mkdir(parents=True, exist_ok=True)
    file_ext = file.filename.split('.')[-1] if '.' in file.filename else 'png'
    if file_ext in ['png', 'jpg', 'jpeg']:  # Можно расширить список допустимых форматов

        filename = f"{uuid4()}.{file_ext}"
        filepath = os.path.join(upload_dir, filename)
        try:
            async with aiofiles.open(filepath, "wb") as buffer:
                while chunk := await file.read(1024 * 1024):  # Читаем по 1MB за раз
                    await buffer.write(chunk)
        except Exception as e:
            raise HTTPException(500, detail=f"Ошибка при сохранении файла: {str(e)}")
        path = f'/api/images/{filename}'
        print(path)
        return path

async def get_image(
    name: str
):
    print(name)
    return FileResponse(f"media/{name}", headers={"Cache-Control": "no-cache"})


async def create_gdz(
        db: orm.Session,
        gdz_str: str,
        file_content: Optional[UploadFile],
        owner_id: str
):
    try:
        gdz_data = schemas.GDZCreate.model_validate_json(gdz_str)
    except ValueError as e:
        print(f"Ошибка валидации: {e}")
        raise
    try:
        user = db.query(models.User).filter_by(id=owner_id).first()
        if gdz_data.is_elite and (user.user_rating is None or user.user_rating < 4.8):
            raise HTTPException(
                status_code=403,
                detail="Недостаточный рейтинг для создания элитного ГДЗ (требуется ≥4.8)"
            )
        filename = None
        if file_content:
            filename = await save_uploaded_file(file_content)

        gdz = models.GDZ(
            description=gdz_data.description,
            full_description=gdz_data.full_description,
            category=gdz_data.category,
            owner_id=owner_id,
            content=filename,
            content_text=gdz_data.content_text,
            price=gdz_data.price,
            is_elite =gdz_data.is_elite
        )

        db.add(gdz)
        db.commit()
        db.refresh(gdz)

        user = db.query(models.User).filter_by(id=owner_id).first()
        if user.has_draft:
            await cleanup_draft(db, owner_id)

        asyncio.create_task(cleanup_old_gdz(db))
        return gdz

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(500, detail=f"Ошибка при создании записи: {str(e)}")


async def get_gdz_by_id(
        db: orm.Session,
        gdz_id: int):
    return db.query(models.GDZ).filter(models.GDZ.id == gdz_id).first()


# async def get_all_gdz_sorted_by_rating(db: orm.Session, descending: bool = True):
#     stmt = select(models.GDZ).where(models.GDZ.rating.is_not(None))
#
#     if descending:
#         stmt = stmt.order_by(models.GDZ.rating.desc())
#     else:
#         stmt = stmt.order_by(models.GDZ.rating.asc())
#
#     result = await db.execute(stmt)
#     return result.scalars().all()


async def get_gdz_by_owner(db: orm.Session, user_id: int):
    return db.query(models.GDZ).filter(models.GDZ.owner_id == user_id).all()

async def is_gdz_free(db: orm.Session, gdz_id: int):
    gdz = await get_gdz_by_id(db, gdz_id)
    return gdz and gdz.price == 0


# async def get_user_purchases(db: orm.Session, user_id: int):
#     stmt = (
#         select(models.GDZ)  # Выбираем GDZ, а не Purchase
#         .join(models.Purchase, models.Purchase.gdz_id == models.GDZ.id)  # Соединяем с Purchase
#         .where(models.Purchase.buyer_id == user_id)  # Только покупки текущего пользователя
#     )
#     result = db.execute(stmt)
#     return result.scalars().all()  # Возвращаем GDZ, а не Purchase

async def get_gdz_by_category(category: str, current_user: schemas.UserInDB, db: orm.Session):
    query = db.query(models.GDZ).filter(models.GDZ.category == category)
    if current_user.user_rating is None or current_user.user_rating < 4.8:
        print(current_user.user_rating)
        query = query.filter(
            or_(
                models.GDZ.is_elite == False,
                models.GDZ.owner_id == current_user.id
            )
        )

    tasks = query.all()
    res = [
        {
            "id": task.id,
            "description": task.description,
            "price": task.price,
            "owner_id": task.owner_id,
            "is_elite": task.is_elite,
            "has_purchased": await get_purchase(db, current_user.id, task.id) is not None
        }
        for task in tasks
    ]
    print(res)
    return res


async def get_purchase(db: orm.Session, user_id: int, gdz_id: int):
    stmt = (
        select(models.Purchase)
        .where(models.Purchase.buyer_id == user_id)
        .where(models.Purchase.gdz_id == gdz_id)
    )
    result = db.execute(stmt)
    return result.scalar_one_or_none()


async def get_gdz_full(
        gdz_id: int,
        db: orm.session,
        current_user: schemas.UserInDB
):
    gdz = await get_gdz_by_id(db, gdz_id)
    if not gdz:
        raise HTTPException(status_code=404, detail="ГДЗ не найдено")

    enforce_elite_access(db, gdz, current_user)

    is_free = gdz.price==0
    is_owner = gdz.owner_id == current_user.id
    has_purchased = await get_purchase(db, current_user.id, gdz_id) is not None

    if not (is_free or is_owner or has_purchased):
        raise HTTPException(
            status_code=403,
            detail="Купи сначала"
        )

    return gdz

async def free_purchase(
        gdz_id: int,
        db: orm.Session,
        current_user: schemas.UserInDB
):
    gdz = await get_gdz_by_id(db, gdz_id)
    if not gdz:
        raise HTTPException(status_code=404, detail="ГДЗ не найдено")

    enforce_elite_access(db, gdz, current_user)
    if gdz.price != 0:
        raise HTTPException(status_code=400, detail="Это ГДЗ не бесплатное")

    existing_purchase = await get_purchase(db, current_user.id, gdz_id)
    if existing_purchase:
        return {"message": "Покупка уже существует"}

    purchase = models.Purchase(
        buyer_id=current_user.id,
        gdz_id=gdz_id,
    )

    db.add(purchase)
    db.commit()
    db.refresh(purchase)

    return {"message": "Запись о покупке создана"}

async def purchase_gdz(
        gdz_id: int,
        db: orm.Session,
        current_user: schemas.UserInDB
):
    gdz = await get_gdz_by_id(db, gdz_id)
    if not gdz:
        raise HTTPException(status_code=404, detail="ГДЗ не найдено")
    existing_purchase = await get_purchase(db, current_user.id, gdz_id)
    if existing_purchase:
        raise HTTPException(status_code=400, detail="Вы уже приобрели это ГДЗ")

    enforce_elite_access(db, gdz, current_user)

    is_free = await is_gdz_free(db, gdz_id)
    if is_free:
        raise HTTPException(status_code=400, detail="Бесплатное ГДЗ не требует покупки")

    confirmation_code = await create_code()

    existing_code = db.query(models.Codes).filter(
        models.Codes.user_id == current_user.id,
        models.Codes.gdz_id == gdz_id
    ).first()

    if existing_code:
        existing_code.code = confirmation_code
        db.commit()
        db.refresh(existing_code)
    else:
        code = models.Codes(
            user_id=current_user.id,
            gdz_id=gdz_id,
            code=confirmation_code
        )
        db.add(code)
        db.commit()
        db.refresh(code)

    return {
        "confirmation_code": str(confirmation_code),
    }

async def create_code():
    return(secrets.randbelow(2**60))


async def validate_signature(
        db: orm.Session,
        user_id: int,
        gdz_id: int,
        signature: int,
):
    n = 160301046244593794374726426877457303604019537423736458260136643925405546154653037172463089669436445456557499425029994701102494179131569495553118775092473011745647436677950345054183103280168169605050154349614937369702539109115434630721210013794356412532578527347021846882486616784364644818143571566741240343519
    e = 3

    keylength = len(long_to_bytes(n))
    decrypted = pow(signature, e, n)
    clearsig = decrypted.to_bytes(keylength, 'big')
    r = re.compile(b'\x00\x01\xff+?\x00(.{20})', re.DOTALL)
    m = r.match(clearsig)

    code = db.execute(
        select(models.Codes.code)
        .where(models.Codes.user_id == user_id)
        .where(models.Codes.gdz_id == gdz_id)
    ).scalar()
    print(m.group(1), bytes.fromhex(sha1(code)))
    if not m:
        return False
    if m.group(1) != bytes.fromhex(sha1(code)):
        return False
    return True


async def confirm_purchase(
        gdz_id: int,
        signature: schemas.Signature,
        db: orm.Session,
        current_user: schemas.UserInDB
):
    gdz = await get_gdz_by_id(db, gdz_id)
    if not gdz:
        raise HTTPException(status_code=404, detail="ГДЗ не найдено")
    existing_purchase = await get_purchase(db, current_user.id, gdz_id)
    if existing_purchase:
        raise HTTPException(status_code=400, detail="Вы уже приобрели это ГДЗ")

    is_free = await is_gdz_free(db, gdz_id)
    if is_free:
        raise HTTPException(status_code=400, detail="Бесплатное ГДЗ не требует покупки")
    if await validate_signature (db, current_user.id, gdz_id, signature.value):

        purchase = models.Purchase(
            buyer_id=current_user.id,
            gdz_id=gdz_id,
        )

        db.add(purchase)
        db.commit()
        db.refresh(purchase)

        print("добавлено")
        return {"message": "Покупка подтверждена", "gdz_id": gdz_id}
    else:
        raise HTTPException(status_code=400, detail="Введено неверное значение")


async def rate_gdz(
        rating: schemas.GDZRatingIn,
        db: orm.Session,
        current_user: schemas.UserInDB
):
    # Получаем ГДЗ со связью с владельцем
    gdz = (
        db.query(models.GDZ)
        .options(orm.joinedload(models.GDZ.user))
        .filter_by(id=rating.gdz_id)
        .first()
    )
    if not gdz:
        raise HTTPException(404, "ГДЗ не найдено")

    enforce_elite_access(db, gdz, current_user)

    # Проверяем, что пользователь не владелец
    if gdz.owner_id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Вы не можете оценивать свои ГДЗ"
        )

    has_purchased = await get_purchase(db, current_user.id, rating.gdz_id)
    if not has_purchased and gdz.price > 0:
        raise HTTPException(
            status_code=403,
            detail="Нельзя оценить ГДЗ без покупки"
        )

    # Проверяем, не оценивал ли уже пользователь это ГДЗ
    existing_rating = (
        db.query(models.GDZRating)
        .filter_by(
            gdz_id=rating.gdz_id,
            user_id=current_user.id
        )
        .first()
    )

    if existing_rating:
        raise HTTPException(
            status_code=400,
            detail="Вы уже оценивали это ГДЗ"
        )

    # Создаем оценку
    new_rating = models.GDZRating(
        gdz_id=rating.gdz_id,
        user_id=current_user.id,
        value=rating.value,
        created_at=datetime.utcnow()
    )
    db.add(new_rating)
    db.commit()

    # Обновляем рейтинг автора ГДЗ
    update_user_rating(db, gdz.owner_id)

    return {
        "detail": "Оценка добавлена",
        "owner_rating": gdz.user.user_rating
    }


def update_user_rating(db: orm.Session, owner_id: int):
    user = db.query(models.User).get(owner_id)
    if not user:
        return

    five_minutes_ago = datetime.utcnow() - timedelta(minutes=5)

    ratings = (
        db.query(models.GDZRating.value)
        .join(models.GDZ)
        .filter(models.GDZ.owner_id == owner_id)
        .filter(models.GDZRating.created_at >= five_minutes_ago)
        .order_by(models.GDZRating.created_at.desc())
        .all()
    )

    if len(ratings) >= 5:
        avg_rating = sum(r[0] for r in ratings) / len(ratings)
        user.user_rating = round(avg_rating, 2)
    else:
        user.user_rating = 0.0

    db.commit()

def enforce_elite_access(db: orm.Session, gdz, user):
    # Обновляем рейтинг пользователя перед проверкой
    
    update_user_rating(db, user.id)
    if gdz.is_elite and gdz.owner_id != user.id:
        if user.user_rating is None or user.user_rating < 4.8:
            raise HTTPException(
                status_code=403,
                detail="Недостаточный рейтинг для доступа к элитному ГДЗ"
            )
DRAFTS_DIR = Path("drafts")
env = Environment(autoescape=False)


async def save_draft(
    db: orm.Session,
    current_user: schemas.UserInDB,
    data: Dict[str, Any] = Body(...)
):
    try:
        draft_data = {
            "description": data.get("description"),
            "full_description": data.get("full_description"),
            "category": data["category"],
            "subject": data.get("subject"),
            "content_text": data.get("content_text"),
            "price": data.get("price"),  # Может быть None
            "is_elite": data.get("is_elite"),
            "gdz_id": data.get("gdz_id")
        }

        await create_or_update_draft(
            db=db,
            owner_id=current_user.id,
            data=draft_data,
        )
        return {"status": "success"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def create_or_update_draft(
    db: orm.Session,
    owner_id: int,
    data: Dict[str, Any] = Body(...),
) -> None:
    try:
        user = db.query(models.User).filter_by(id=owner_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        user.has_draft = True
        db.commit()

        draft_id = owner_id
        filename = f"draft_{owner_id}.txt"
        file_path = DRAFTS_DIR / filename

        draft_content = {
            "owner_id": owner_id,
            "description": data.get("description", ""),
            "full_description": data.get("full_description"),
            "category": data.get("category", ""),
            "subject": data.get("subject", ""),
            "content_text": data.get("content_text", ""),
            "price": data.get("price"),  # Сохраняем как есть (может быть None)
            "is_elite": data.get("is_elite", False),
        }

        await save_draft_to_file(draft_content, file_path)
        return

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка сохранения черновика: {str(e)}")


async def save_draft_to_file(draft_content: Dict[str, Any], file_path: Path) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)

    for key in ['description', 'full_description', 'content_text']:
        if key in draft_content and draft_content[key] is not None:
            draft_content[key] = draft_content[key].replace('\n', '\\n')

    template_lines = []
    for key, value in draft_content.items():
        if key == "is_elite":
            template_lines.append(f'    "{key}": {{% if {key} %}}true{{% else %}}false{{% endif %}},')
        elif value is None:
            template_lines.append(f'    "{key}": null,')
        elif isinstance(value, (int, float)) or key in ["id", "owner_id", "price"]:
            template_lines.append(f'    "{key}": {{{{ {key} }}}},')
        else:
            template_lines.append(f'    "{key}": "{{{{ {key} }}}}",')

    template_lines[-1] = template_lines[-1].rstrip(',')
    template_string = '{\n' + '\n'.join(template_lines) + '\n}'
    template = env.from_string(template_string)
    rendered_content = template.render(**draft_content)

    async with aiofiles.open(file_path.with_suffix('.txt'), "w", encoding="utf-8") as f:
        await f.write(rendered_content)

async def get_draft(
        db: orm.Session,
        current_user: schemas.UserInDB
):
    user = db.query(models.User).filter_by(id=current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    if not user.has_draft:
        return schemas.DraftData(
            description="",
            category="",
            subject="",
            content_text="",
            price=0,
            is_elite=False,
        )
    filename = f"draft_{current_user.id}.txt"
    file_path = DRAFTS_DIR / filename

    try:
        data = await read_draft_from_file(Path(file_path))
        print("data", data)
        if data.get("owner_id") != current_user.id:
            raise HTTPException(status_code=403, detail="Вы не можете смотреть чужие черновики")

        return schemas.DraftData(
            description=data.get("description"),
            full_description = data.get("full_description"),
            category=data.get("category"),
            subject=data.get("subject"),
            content_text=data.get("content_text"),
            price=data.get("price"),
            is_elite=data.get("is_elite"),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка чтения черновика: {str(e)}")


async def read_draft_from_file(file_path: Path) -> dict:
    try:
        async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
            content = await f.read()
            data = json.loads(content)

            # Восстанавливаем переносы строк в текстовых полях
            for key in ['description', 'full_description', 'content_text']:
                if key in data and data[key] is not None and isinstance(data[key], str):
                    data[key] = data[key].replace('\\n', '\n')

            return data
    except json.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON {file_path}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Некорректный JSON в черновике: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка чтения черновика: {str(e)}")


async def cleanup_draft(db: orm.Session, owner_id: str, drafts_dir: Path = "drafts") -> None:
    try:
        user = db.query(models.User).filter_by(id=owner_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        user.has_draft = False
        db.commit()

        drafts_dir = Path(drafts_dir) if isinstance(drafts_dir, str) else drafts_dir
        filename = f"draft_{owner_id}.json"
        file_path = drafts_dir / filename


        file_path.parent.mkdir(parents=True, exist_ok=True)

        async with aiofiles.open(file_path, "w", encoding="utf-8") as f:
            await f.write("")

        print(f"Содержимое файла черновика {file_path} очищено")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при очистке черновика: {str(e)}")

    except Exception as e:
        db.rollback()
        print(f"Ошибка при очистке черновика: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка при очистке черновика: {str(e)}")


async def cleanup_old_gdz(db: orm.Session):
    MAX_GDZ = 100
    try:
        total = db.query(models.GDZ).count()
        print(total)
        if total > MAX_GDZ:
            old_gdz = (
                db.query(models.GDZ)
                .order_by(models.GDZ.id.asc())
                .limit(total - MAX_GDZ)
                .all()
            )


            gdz_to_delete: List[int] = []
            file_paths: List[str] = []


            for gdz in old_gdz:
                gdz_to_delete.append(gdz.id)
                file_name = gdz.content.split("/")[-1]
                print(file_name)
                file_path = os.path.join("media/", os.path.basename(file_name))
                file_paths.append(file_path)

            print(gdz_to_delete)
            print(file_paths)

            purchase_count =(db.query(models.Purchase).
             filter(models.Purchase.gdz_id.in_(gdz_to_delete)).
             delete())
            print(purchase_count)

            (db.query(models.Codes).
             filter(models.Codes.gdz_id.in_(gdz_to_delete)).
             delete())

            (db.query(models.GDZRating).
             filter(models.GDZRating.gdz_id.in_(gdz_to_delete)).
             delete())

            affected_users = db.query(models.GDZ.owner_id).filter(models.GDZ.id.in_(gdz_to_delete)).distinct().all()
            print(affected_users)
            for user_id in [u.owner_id for u in affected_users]:
                update_user_rating(db, user_id)

            a = db.query(models.GDZ).filter(models.GDZ.id.in_(gdz_to_delete)).delete()
            db.commit()

            for file_path in file_paths:
                try:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                except Exception as e:
                    raise HTTPException(status_code=500, detail=f"Ошибка при удалении файла: {str(e)}")


    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при очистке ГДЗ: {str(e)}")

async def get_user_gdz_ratings_last(db: orm.Session, user_id: int) -> List[schemas.GDZRatingOut]:
    five_minutes_ago = datetime.utcnow() - timedelta(minutes=5)

    # Базовый запрос
    query = (
        db.query(models.GDZRating)
        .join(models.GDZ)
        .filter(models.GDZ.owner_id == user_id)
        .filter(models.GDZRating.created_at >= five_minutes_ago)
    )

    ratings = query.order_by(models.GDZRating.created_at.asc()).all()
    
    # Преобразуем в Pydantic модель
    return [schemas.GDZRatingOut.from_orm(rating) for rating in ratings]