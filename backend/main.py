from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
from services import get_db
import security
import services
import schemas

app = FastAPI()

origins = [
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/register")
async def register(user: schemas.UserCreate, db: orm.Session = Depends(services.get_db)):
    user_ex = await services.get_user(db, user.username)
    if user_ex:
        raise HTTPException(status_code=400, detail="Username already registered")
    user = await services.create_user(db, user)
    return await services.create_access_token(data={"sub": user.username})

@app.post("/token")
async def login(form_data:security.OAuth2PasswordRequestForm = Depends(), db:orm.Session = Depends(services.get_db)):
    user = await services.get_user(db, form_data.username)
    if not services.authenticate_user(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = services.create_access_token(data={"sub": user.username})

#@router.post("/gdz/create")
#def create_gdz_view(gdz_data: GDZCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
 #   return create_gdz(db, gdz_data, owner_username=current_user.username)

