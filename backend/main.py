from fastapi import FastAPI, HTTPException, Depends, security, Request, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
from services import get_db
import services
import models
import schemas
from PIL import Image  # Для работы с изображениями
import io

app = FastAPI()

ALLOWED_TYPES = {
    "image/jpeg": "jpg",
    "image/png": "png",
    "image/webp": "webp",
    "application/pdf": "pdf",
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
    gdz_data = schemas.GDZBase.model_validate_json(gdz_str)
    return await services.create_gdz(db, gdz_data, content_file, owner_id=current_user.id)


@app.get("/gdz/", response_model=list[schemas.GDZPublic])
def get_all_gdz(db: Session = Depends(get_db)):
    return db.query(models.GDZ).all()

@app.get("/gdz/{gdz_id}", response_model=schemas.GDZPublic)
async def get_gdz_by_id(gdz_id: int, db: Session = Depends(get_db)):
    gdz = services.get_gdz_by_id(db, gdz_id)
    if not gdz:
        raise HTTPException(status_code=404, detail="ГДЗ не найдено")
    return gdz


@app.get("/gdz/sorted", response_model=list[schemas.GDZPublic])
def get_sorted_gdz(
    db: Session = Depends(get_db),
    order: str = "desc"):
    descending = order.lower() != "asc"
    return services.get_all_gdz_sorted_by_rating(db, descending)

@app.get("/gdz/by-category/{category}", response_model=list[schemas.GDZPublic])
def get_gdz_by_category(category: str, db: Session = Depends(get_db)):
    return db.query(models.GDZ).filter(models.GDZ.category == category).all()

@app.get("/")
async def root():
    return {"Messages": "GDZ"}