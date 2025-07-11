#            /$$                 /$$ /$$                               /$$
#           | $$                | $$| $$                              | $$
#   /$$$$$$$| $$$$$$$   /$$$$$$ | $$| $$ /$$  /$$  /$$  /$$$$$$   /$$$$$$$  /$$$$$$  /$$$$$$$   /$$$$$$$  /$$$$$$
#  /$$_____/| $$__  $$ /$$__  $$| $$| $$| $$ | $$ | $$ /$$__  $$ /$$__  $$ |____  $$| $$__  $$ /$$_____/ /$$__  $$
# |  $$$$$$ | $$  \ $$| $$$$$$$$| $$| $$| $$ | $$ | $$| $$$$$$$$| $$  | $$  /$$$$$$$| $$  \ $$| $$      | $$$$$$$$
#  \____  $$| $$  | $$| $$_____/| $$| $$| $$ | $$ | $$| $$_____/| $$  | $$ /$$__  $$| $$  | $$| $$      | $$_____/
#  /$$$$$$$/| $$  | $$|  $$$$$$$| $$| $$|  $$$$$/$$$$/|  $$$$$$$|  $$$$$$$|  $$$$$$$| $$  | $$|  $$$$$$$|  $$$$$$$
# |_______/ |__/  |__/ \_______/|__/|__/ \_____/\___/  \_______/ \_______/ \_______/|__/  |__/ \_______/ \_______/
#                                           Team: Sirotkin Nikita, Prudnikov Egor, Prudnikov Dmitry, Makhrin Gleb

from fastapi import (
    FastAPI,
    HTTPException,
    Depends,
    security,
    Request,
    UploadFile,
    File,
    Form,
    Body,
)
from typing import List, Dict
from fastapi.middleware.cors import CORSMiddleware
import sqlalchemy.orm as orm
from services import get_db
import services
import models
import schemas
from typing import List, Dict, Optional, Any
from fastapi import Depends, status
from sqlalchemy.orm import Session
from pathlib import Path
from threading import Lock

rating_lock = Lock()

app = FastAPI()

origins = ["http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/register")
<<<<<<< HEAD
async def register(
    request: Request,
    user: schemas.UserCreate,
    db: orm.Session = Depends(services.get_db),
):
    print("Получены данные:", await request.json())
=======
async def register(request: Request, user: schemas.UserCreate, db: orm.Session = Depends(services.get_db)):
>>>>>>> 090bcf9cc2c4398ddef8d40ef67afd210566db29
    user_ex = await services.get_user(db, user.username)
    if user_ex:
        raise HTTPException(status_code=400, detail="username already registered")

    try:
        user_db = await services.create_user(db, user)
        return await services.create_access_token(user_db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/token")
async def username(
    form_data: security.OAuth2PasswordRequestForm = Depends(),
    db: orm.Session = Depends(services.get_db),
):
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
    current_user: models.User = Depends(services.get_current_user),
):
    with rating_lock:
        return await services.get_profile_data(db, current_user)


@app.get("/category", response_model=List[str])
async def get_subjects(db: Session = Depends(get_db)):
    subjects = db.query(models.Subjects.category).distinct().all()
    return [subject[0] for subject in subjects]


@app.get("/subjects/{category}", response_model=List[str])
<<<<<<< HEAD
async def get_subjects_by_category(category: str, db: Session = Depends(get_db)):
    a = await services.get_subjects_by_category(db, category)
    print(a)
    return a

=======
async def get_subjects_by_category(
    category: str,
    db: Session = Depends(get_db)
):
    return await services.get_subjects_by_category(db, category)
>>>>>>> 090bcf9cc2c4398ddef8d40ef67afd210566db29
    return await services.get_subjects_by_category(db, category)

@app.post("/gdz/create")
async def create_gdz_en(
    content_file: UploadFile = File(None),
    gdz_str: str = Form(...),
    db: orm.Session = Depends(get_db),
    current_user=Depends(services.get_current_user),
):
    return await services.create_gdz(
        db, gdz_str, content_file, owner_id=current_user.id
    )


@app.get("/gdz_category/{category}", response_model=list[schemas.GDZPublicShort])
async def get_gdz_by_category(
    category: str,
    limit: int = None,
    current_user: models.User = Depends(services.get_current_user),
    db: Session = Depends(get_db),
):
    return await services.get_gdz_by_category(
        category=category, current_user=current_user, db=db, limit=limit
    )


@app.get("/gdz/{gdz_id}/full", response_model=schemas.GDZPrivate)
async def get_gdz_full(
    gdz_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(services.get_current_user),
):
    return await services.get_gdz_full(gdz_id, db, current_user)


@app.get("/images/{image_name}")
async def get_image(image_name: str, db: orm.Session = Depends(services.get_db)):
    return await services.get_image(name=image_name)


@app.post("/gdz/{gdz_id}/free-purchase", status_code=201)
async def free_purchase(
    gdz_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(services.get_current_user),
):
    return await services.free_purchase(gdz_id, db, current_user)


@app.post("/gdz/{gdz_id}/purchase", status_code=status.HTTP_201_CREATED)
async def purchase_gdz(
    gdz_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(services.get_current_user),
):
    return await services.purchase_gdz(gdz_id, db, current_user)


@app.post("/gdz/{gdz_id}/confirm-purchase", status_code=201)
async def confirm_purchase(
    gdz_id: int,
    signature: schemas.Signature,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(services.get_current_user),
):
    return await services.confirm_purchase(gdz_id, signature, db, current_user)


@app.post("/gdz/rate")
async def rate_gdz(
    rating: schemas.GDZRatingIn,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(services.get_current_user),
):
    with rating_lock:
        return await services.rate_gdz(rating, db, current_user)


@app.post("/gdz/save_draft")
async def save_draft(
    data: Dict[str, Any] = Body(...),
    db: orm.Session = Depends(services.get_db),
    current_user: models.User = Depends(services.get_current_user),
):
    return await services.save_draft(db, current_user, data)


@app.get("/gdz/get_draft", response_model=schemas.DraftData)
async def get_draft(
    db: orm.Session = Depends(services.get_db),
    current_user: models.User = Depends(services.get_current_user),
):
    return await services.get_draft(db, current_user)


@app.get("/gdz/my/ratings", response_model=List[schemas.GDZRatingOut])
async def get_my_gdz_ratings(
    db: orm.Session = Depends(get_db),
    current_user: models.User = Depends(services.get_current_user),
):
    ratings = await services.get_user_gdz_ratings_last(db, current_user.id)
    return ratings


@app.get("/")
async def root():
    return {"Messages": "GDZ"}
