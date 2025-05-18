from fastapi import FastAPI, HTTPException, Depends, security, Request, UploadFile, File, Form
from typing import List, Dict
from fastapi.middleware.cors import CORSMiddleware
import sqlalchemy.orm as orm
from services import get_db
import services
import models
import schemas
from typing import List, Dict, Union
from fastapi import Depends
from sqlalchemy.orm import Session

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


@app.get("/users/me", response_model=schemas.User)
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
    purchased_gdz = await services.get_user_purchases(db, user.id)
    gdz_list = []

    for gdz in created_gdz + purchased_gdz:
        gdz_list.append({
            "id": gdz.id,
            "description": gdz.description,
            "category": gdz.category,
            "content": gdz.content,
            "content_text": gdz.content_text,
            "price": gdz.price,
            "rating": gdz.rating,
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


@app.post("/gdz/create")
async def create_gdz_en(
        content_file: UploadFile = File(...),
        gdz_str: str = Form(...),
        db: orm.Session = Depends(get_db),
        current_user=Depends(services.get_current_user)
):
    try:
        print(f"Получен файл: {content_file.filename}")  # Проверяем получение файла
        print(f"Размер файла: {content_file.size}")
        gdz_data = schemas.GDZCreate.model_validate_json(gdz_str)
        print(gdz_data)
    except ValueError as e:
        print(f"Ошибка валидации: {e}")
        raise
    return await services.create_gdz(db, gdz_data, content_file, owner_id=current_user.id)


@app.get("/subjects/{category}", response_model=List[Dict[str, str]])
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
    return [
        {"subject_name": subject.subject_name, "slug": subject.paths}
        for subject in subjects
    ]


# @app.get("/gdz/", response_model=list[schemas.GDZPublic])
# def get_all_gdz(db: Session = Depends(get_db)):
#     return db.query(models.GDZ).all()

# @app.get("/gdz/sorted", response_model=list[schemas.GDZPublic])
# async def get_sorted_gdz(db: Session = Depends(get_db)):
#     result = db.execute(
#         select(models.GDZ)
#         .order_by(models.GDZ.rating.desc())
#         .limit(10)
#     )
#     gdz_list = result.scalars().all()
#
#     # Отладочная печать
#     for gdz in gdz_list:
#         print(f"ID: {gdz.id}, Rating: {gdz.rating}, Desc: {gdz.description}")
#
#     return gdz_list


@app.get("/gdz_category/{category}", response_model=list[schemas.GDZPublicShort])
def get_gdz_by_category(category: str, db: Session = Depends(get_db)):
    tasks = ((db.query(models.GDZ)
     .filter(models.GDZ.category == category))
     .all())
    return [
            {
                "id": task.id,
                "description": task.description,
                "price": task.price,
                # Добавьте другие необходимые поля
            }
            for task in tasks
        ]

@app.get("/gdz/{gdz_id}", response_model=schemas.GDZPublic)
async def get_gdz_by_id(gdz_id: int, db: Session = Depends(get_db)):
    gdz = await services.get_gdz_by_id(db, gdz_id)
    if not gdz:
        raise HTTPException(status_code=404, detail="ГДЗ не найдено")
    return gdz


@app.get("/gdz/{gdz_id}/full", response_model=schemas.GDZPrivate)
async def get_gdz_full(
        gdz_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(services.get_current_user)
):
    # Проверяем права доступа
    gdz = await services.get_gdz_by_id(db, gdz_id)
    if not gdz:
        raise HTTPException(status_code=404, detail="ГДЗ не найдено")

    # Проверяем, является ли пользователь владельцем или покупателем
    is_owner = gdz.owner_id == current_user.id
    has_purchased = await services.get_purchase(db, current_user.id, gdz_id) is not None

    if not (is_owner or has_purchased):
        raise HTTPException(
            status_code=403,
            detail="Купи сначала"
        )

    return gdz


@app.post("/gdz/{gdz_id}/purchase", status_code=201)
async def purchase_gdz(
        gdz_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(services.get_current_user)
):
    # Проверяем существование ГДЗ
    gdz = await services.get_gdz_by_id(db, gdz_id)
    if not gdz:
        raise HTTPException(status_code=404, detail="ГДЗ не найдено")

    # Проверяем, не куплено ли уже
    existing_purchase = await services.get_purchase(db, current_user.id, gdz_id)
    if existing_purchase:
        raise HTTPException(status_code=400, detail="Вы уже приобрели это ГДЗ")

    # Определяем тип ГДЗ (бесплатное/платное)
    if gdz.price==0:  # Добавьте это поле в модель GDZ
        purchase = models.Purchase(
            buyer_id=current_user.id,
            gdz_id=gdz_id,
        )
        db.add(purchase)
        db.commit()
        db.refresh(purchase)
        return {"message": "Бесплатное ГДЗ успешно получено", "gdz_id": gdz_id}
    else:
        confirmation_code = 5578

        code = models.Codes(
            user_id = current_user.id,
            gdz_id = gdz_id,
            code =  confirmation_code
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
    if await services.validate_signature (db, current_user.id, gdz_id, signature.value):

        purchase = models.Purchase(
            buyer_id=current_user.id,
            gdz_id=gdz_id,
        )

        db.add(purchase)
        db.commit()
        db.refresh(purchase)

        return {"message": "Покупка подтверждена", "gdz_id": gdz_id}
    else:
            print("ошибка")

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


@app.get("/")
async def root():
    return {"Messages": "GDZ"}