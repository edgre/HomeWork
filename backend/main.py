from fastapi import FastAPI, HTTPException, Depends, security, Request, UploadFile, File, Form, Body
from typing import List, Dict
from fastapi.middleware.cors import CORSMiddleware
import sqlalchemy.orm as orm
from services import get_db
import services
import models
import schemas
from typing import List, Dict, Any
from fastapi import Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from pathlib import Path

app = FastAPI()

ALLOWED_TYPES = {
    "image/jpeg": "jpg",
    "image/png": "png",
    "text/plain": "txt"
}

origins = [
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/register")
async def register(request: Request, user: schemas.UserCreate, db: orm.Session = Depends(services.get_db)):
    print("Получены данные:", await request.json())
    user_ex = await services.get_user(db, user.username)
    if user_ex:
        raise HTTPException(status_code=400, detail="username already registered")

    try:
        user_db = await services.create_user(db, user)
        return await services.create_access_token(user_db)
    except Exception as e:
        print("Ошибка при регистрации:", str(e))
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/token")
async def username(form_data: security.OAuth2PasswordRequestForm = Depends(), db:orm.Session = Depends(services.get_db)):
    user = await services.get_user(db, form_data.username)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    if not await services.authenticate_user(db, form_data.username, form_data.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return await services.create_access_token(user)


@app.get("/users/me", response_model=schemas.UserInDB)
async def get_user(user: schemas.User = Depends(services.get_current_user)):
    return user

@app.get("/profile/data", response_model=schemas.UserProfileResponse)
async def get_profile_data(
        db: Session = Depends(get_db),
        current_user: models.User = Depends(services.get_current_user)
):
    # Получаем данные пользователя напрямую из базы данных
    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Получаем ГДЗ пользователя
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
        #"is_elite": user.is_elite,
        "gdz_list": gdz_list
    }

@app.get("/category", response_model=List[str])
async def get_subjects(db: Session = Depends(get_db)):
    subjects = db.query(models.Subjects.category).distinct().all()
    return [subject[0] for subject in subjects]


@app.get("/subjects/{category}", response_model=List[str])
def get_subjects_by_category(
    category: str,
    db: Session = Depends(get_db)
):
    subjects = db.query(
        models.Subjects.subject_name,
        models.Subjects.paths
    ).filter(
        models.Subjects.category == category
    ).all()
    return [ subject.subject_name for subject in subjects]

@app.post("/gdz/create")
async def create_gdz_en(
        content_file: UploadFile = File(...),
        gdz_str: str = Form(...),
        db: orm.Session = Depends(get_db),
        current_user=Depends(services.get_current_user)
):
    try:
        print(f"Получен файл: {content_file.filename}")
        print(f"Размер файла: {content_file.size}")
        gdz_data = schemas.GDZCreate.model_validate_json(gdz_str)
    except ValueError as e:
        print(f"Ошибка валидации: {e}")
        raise
    return await services.create_gdz(db, gdz_data, content_file, owner_id=current_user.id)


@app.get("/gdz_category/{category}", response_model=list[schemas.GDZPublicShort])
async def get_gdz_by_category(
        category: str,
        current_user: models.User = Depends(services.get_current_user),
        db: Session = Depends(get_db)):
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
            "has_purchased": await services.get_purchase(db, current_user.id, task.id) is not None
        }
        for task in tasks
    ]
    print(res)
    return res

# @app.get("/gdz/{gdz_id}", response_model=schemas.GDZPublic)
# async def get_gdz_by_id(gdz_id: int, db: Session = Depends(get_db)):
#     gdz = await services.get_gdz_by_id(db, gdz_id)
#     if not gdz:
#         raise HTTPException(status_code=404, detail="ГДЗ не найдено")
#     return gdz


@app.get("/gdz/{gdz_id}/full", response_model=schemas.GDZPrivate)
async def get_gdz_full(
        gdz_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(services.get_current_user)
):
    gdz = await services.get_gdz_by_id(db, gdz_id)
    if not gdz:
        raise HTTPException(status_code=404, detail="ГДЗ не найдено")

    services.enforce_elite_access(gdz, current_user)

    # Проверяем, является ли пользователь владельцем или покупателем
    is_free = gdz.price==0
    is_owner = gdz.owner_id == current_user.id
    has_purchased = await services.get_purchase(db, current_user.id, gdz_id) is not None

    if not (is_free or is_owner or has_purchased):
        raise HTTPException(
            status_code=403,
            detail="Купи сначала"
        )

    return gdz


@app.get("/images/{image_name}")
async def get_image(
    image_name: str,
    db: orm.Session = Depends(services.get_db)
):
    return await services.get_image(name=image_name)


@app.post("/gdz/{gdz_id}/free-purchase", status_code=201)
async def free_purchase(
        gdz_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(services.get_current_user)
):
    gdz = await services.get_gdz_by_id(db, gdz_id)
    if not gdz:
        raise HTTPException(status_code=404, detail="ГДЗ не найдено")

    # Проверяем, что ГДЗ действительно бесплатное
    if gdz.price != 0:
        raise HTTPException(status_code=400, detail="Это ГДЗ не бесплатное")

    # Проверяем, что у пользователя еще нет этой покупки
    existing_purchase = await services.get_purchase(db, current_user.id, gdz_id)
    if existing_purchase:
        return {"message": "Покупка уже существует"}

    # Создаем запись о покупке
    purchase = models.Purchase(
        buyer_id=current_user.id,
        gdz_id=gdz_id,
    )

    db.add(purchase)
    db.commit()
    db.refresh(purchase)

    return {"message": "Запись о покупке создана"}

@app.post("/gdz/{gdz_id}/purchase", status_code=status.HTTP_201_CREATED)
async def purchase_gdz(
        gdz_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(services.get_current_user)
):
    gdz = await services.get_gdz_by_id(db, gdz_id)
    if not gdz:
        raise HTTPException(status_code=404, detail="ГДЗ не найдено")
    existing_purchase = await services.get_purchase(db, current_user.id, gdz_id)
    if existing_purchase:
        raise HTTPException(status_code=400, detail="Вы уже приобрели это ГДЗ")

    # Проверяем, бесплатное ли ГДЗ
    is_free = await services.is_gdz_free(db, gdz_id)
    if is_free:
        raise HTTPException(status_code=400, detail="Бесплатное ГДЗ не требует покупки")

    # Генерируем код подтверждения
    confirmation_code = await services.create_code()

    # Ищем существующую запись в таблице Codes
    existing_code = db.query(models.Codes).filter(
        models.Codes.user_id == current_user.id,
        models.Codes.gdz_id == gdz_id
    ).first()

    if existing_code:
        # Если запись существует, обновляем поле code
        existing_code.code = confirmation_code
        db.commit()
        db.refresh(existing_code)
    else:
        # Если записи нет, создаем новую
        code = models.Codes(
            user_id=current_user.id,
            gdz_id=gdz_id,
            code=confirmation_code
        )
        db.add(code)
        db.commit()
        db.refresh(code)

    return {
        "confirmation_code": confirmation_code,
    }


@app.post("/gdz/{gdz_id}/confirm-purchase", status_code=201)
async def confirm_purchase(
        gdz_id: int,
        signature: schemas.Signature,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(services.get_current_user)
):
    gdz = await services.get_gdz_by_id(db, gdz_id)
    if not gdz:
        raise HTTPException(status_code=404, detail="ГДЗ не найдено")
    existing_purchase = await services.get_purchase(db, current_user.id, gdz_id)
    if existing_purchase:
        raise HTTPException(status_code=400, detail="Вы уже приобрели это ГДЗ")

    # Проверяем, бесплатное ли ГДЗ
    is_free = await services.is_gdz_free(db, gdz_id)
    if is_free:
        raise HTTPException(status_code=400, detail="Бесплатное ГДЗ не требует покупки")
    if await services.validate_signature (db, current_user.id, gdz_id, signature.value):

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



@app.post("/gdz/rate")
async def rate_gdz(
        rating: schemas.GDZRatingIn,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(services.get_current_user)
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

    # Проверяем, что пользователь не владелец
    if gdz.owner_id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Вы не можете оценивать свои ГДЗ"
        )

    has_purchased = await services.get_purchase(db, current_user.id, rating.gdz_id)
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
        value=rating.value
    )
    db.add(new_rating)
    db.commit()

    # Обновляем рейтинг автора ГДЗ
    services.update_user_rating(db, gdz.owner_id)

    return {
        "detail": "Оценка добавлена",
        "owner_rating": gdz.user.user_rating
    }

@app.post("/gdz/save_draft")
async def save_draft(
    data: Dict[str, Any] = Body(...),
    db: orm.Session = Depends(services.get_db),
    current_user: models.User = Depends(services.get_current_user)
):
    try:
        # Проверяем наличие обязательных полей
        required_fields = {"category"}  # category обязательное, остальные необязательные
        missing_fields = required_fields - set(data.keys())
        if missing_fields:
            raise HTTPException(status_code=400, detail=f"Отсутствуют обязательные поля: {missing_fields}")

        # Формируем draft_data, устанавливая значения по умолчанию для необязательных полей
        draft_data = {
            "description": data.get("description"),
            "full_description": data.get("full_description"),
            "category": data["category"],  # Обязательное поле
            "subject": data.get("subject"),
            "content_text": data.get("content_text"),
            "price": data.get("price"),
            "is_elite": data.get("is_elite"),
            "gdz_id": data.get("gdz_id")
        }
        print(draft_data)

        await services.create_or_update_draft(
            db=db,
            owner_id=current_user.id,
            data=draft_data,
        )
        return {"status": "success"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


DRAFTS_DIR = "drafts"
drafts_dir = Path(DRAFTS_DIR)

@app.get("/gdz/get_draft", response_model=schemas.DraftData)
async def get_draft(
        db: orm.Session = Depends(services.get_db),
        current_user: models.User = Depends(services.get_current_user)
):
    # Проверяем, существует ли пользователь
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
            gdz_id=None
        )
    filename = f"draft_{current_user.id}.txt"
    file_path = drafts_dir / filename

    try:
        # Читаем данные из файла
        data = await services.read_draft_from_file(Path(file_path))
        print("data", data)
        # Проверяем, что черновик принадлежит текущему пользователю
        if data.get("owner_id") != current_user.id:
            raise HTTPException(status_code=403, detail="Вы не можете смотреть чужие черновики")

        # Возвращаем данные в формате schemas.DraftData
        return schemas.DraftData(
            description=data.get("description"),
            category=data.get("category"),
            subject=data.get("subject"),
            content_text=data.get("content_text"),
            price=data.get("price"),
            is_elite=data.get("is_elite"),
            gdz_id=data.get("gdz_id")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка чтения черновика: {str(e)}")


@app.get("/")
async def root():
    return {"Messages": "GDZ"}
