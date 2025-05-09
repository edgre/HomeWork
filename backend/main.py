from fastapi import FastAPI, HTTPException, Depends, security, Request
from fastapi.middleware.cors import CORSMiddleware
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
from services import get_db
import services
import schemas

app = FastAPI()

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
        token = services.create_access_token(data={"sub": user_db.username})
        return {"access_token": token}
    except Exception as e:
        print("Ошибка при регистрации:", str(e))
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/token")
async def username(form_data: security.OAuth2PasswordRequestForm = Depends(), db:orm.Session = Depends(services.get_db)):
    user = await services.get_user(db, form_data.username)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    if not services.authenticate_user(db, form_data.username, form_data.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return services.create_access_token(data={"sub": user.username})

#@router.post("/gdz/create")
#def create_gdz_view(gdz_data: GDZCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
 #   return create_gdz(db, gdz_data, owner_username=current_user.username)

@app.get("/")
async def root():
    return {"Messages": "GDZ"}