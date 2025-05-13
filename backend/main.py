from fastapi import FastAPI, HTTPException, Depends, security, Request, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
from sqlalchemy import select, desc, func
from services import get_db
import services
import models
import schemas
import random
from PIL import Image  # Для работы с изображениями
import io

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


@app.post("/gdz/create")
async def create_gdz_en(
        content_file: UploadFile = File(...),
        gdz_str: str = Form(...),
        db: orm.Session = Depends(get_db),
        current_user=Depends(services.get_current_user)
):
    print(f"Получен файл: {content_file.filename}")  # Проверяем получение файла
    print(f"Размер файла: {content_file.size}")
    print(gdz_str)
    try:
        gdz_data = schemas.GDZCreate.model_validate_json(gdz_str)
    except ValueError as e:
        print(f"Ошибка валидации: {e}")
        raise
    return await services.create_gdz(db, gdz_data, content_file, owner_id=current_user.id)

@app.get("/gdz/", response_model=list[schemas.GDZPublic])
def get_all_gdz(db: Session = Depends(get_db)):
    return db.query(models.GDZ).all()


@app.get("/gdz/sorted", response_model=list[schemas.GDZPublic])
async def get_sorted_gdz(db: Session = Depends(get_db)):
    result = db.execute(
        select(models.GDZ)
        .order_by(models.GDZ.rating.desc())
        .limit(10)
    )
    gdz_list = result.scalars().all()

    # Отладочная печать
    for gdz in gdz_list:
        print(f"ID: {gdz.id}, Rating: {gdz.rating}, Desc: {gdz.description}")

    return gdz_list


# @app.get("/gdz/by-category/{category}/{subject}", response_model=list[schemas.GDZPublic])
# def get_gdz_by_category(category: str, subject db: Session = Depends(get_db)):
#     return (db.query(models.GDZ)
#             .filter(models.GDZ.category == category)
#             .filter (models.GDZ.subject == subject)
#             .all())




@app.get("/gdz/my", response_model=list[schemas.GDZPrivate])
async def get_my_gdz(
        db: Session = Depends(get_db),
        current_user: models.User = Depends(services.get_current_user)
):
    # Получаем ГДЗ, созданные пользователем
    created_gdz = await services.get_gdz_by_owner(db, current_user.id)

    # Получаем купленные ГДЗ
    purchased_gdz = await services.get_user_purchases(db, current_user.id)

    return created_gdz + purchased_gdz


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


app.get("/gdz/by-filter/", response_model=list[schemas.GDZPublic])


async def get_gdz_by_filter(
        category: str = None,  # Ступень образования (например: "9", "11", "ege")
        subject: str = None,  # Предмет (например: "Математика", "Физика")
        db: Session = Depends(get_db)
):
    query = db.query(models.GDZ)

    if category:
        query = query.filter(models.GDZ.category == category)
    if subject:
        query = query.filter(models.GDZ.subject == subject)

    return query.all()


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
        confirmation_code = random.randint(1000, 9999)

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
        signature: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(services.get_current_user)
):

    if await services.validate_signature (db, gdz_id, current_user.id, signature):

        purchase = models.Purchase(
            buyer_id=current_user.id,
            gdz_id=gdz_id,
            is_paid=True,
        )

        db.add(purchase)
        db.commit()
        db.refresh(purchase)

        return {"message": "Покупка подтверждена", "gdz_id": gdz_id}
    else:
            print("ошибка")





@app.get("/")
async def root():
    return {"Messages": "GDZ"}