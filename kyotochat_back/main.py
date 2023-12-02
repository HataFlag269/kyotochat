from fastapi import BackgroundTasks, FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from models import User, UserCredentials, SessionLocal, DATABASE_URL
from fastapi import BackgroundTasks, FastAPI, Request, HTTPException, status
from models import User, UserCredentials, SessionLocal, DATABASE_URL
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from passlib.hash import bcrypt
from fastapi.middleware.cors import CORSMiddleware
from databases import Database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, joinedload, lazyload 
import sqlalchemy

app = FastAPI()
database = Database(DATABASE_URL, force_rollback=True)
metadata = sqlalchemy.MetaData()
Base = declarative_base()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return await app.handle(request=request)


@app.get("/a")
async def a():
    return {"aaa"}

@app.post("/login")
async def login(
    request: Request,
    credentials: UserCredentials,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    email = credentials.email
    password = credentials.password
    user = (
        db.query(User)
        .options(joinedload(User.chat_logs))
        .filter(User.email == email)
        .first()
    )
    if user and bcrypt.verify(password, user.password):
        background_tasks.add_task(some_background_task, user.email)
        return {"msg": "Login successful"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
    )

