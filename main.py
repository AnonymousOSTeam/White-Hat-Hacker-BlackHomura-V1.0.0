from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional, List
from sqlmodel import Session, select
from jose import JWTError, jwt
from passlib.context import CryptContext
import os

from .models import User, Incident
from .db import engine, create_db_and_tables, get_session

app = FastAPI(title="BlackHomura API")

# config
SECRET_KEY = os.getenv("SECRET_KEY", "change_me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserCreate(BaseModel):
    username: str
    password: str
    role: Optional[str] = "viewer"

class IncidentCreate(BaseModel):
    title: str
    description: str

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(session: Session, username: str, password: str):
    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == token_data.username)).first()
        if user is None:
            raise credentials_exception
        return user

@app.post("/auth/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    with Session(engine) as session:
        user = authenticate_user(session, form_data.username, form_data.password)
        if not user:
            raise HTTPException(status_code=401, detail="Incorrect username or password")
        access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users", status_code=201)
def create_user(u: UserCreate, current_user: User = Depends(get_current_user)):
    # Only admin can create users
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough privileges")
    with Session(engine) as session:
        user = User(username=u.username, hashed_password=get_password_hash(u.password), role=u.role)
        session.add(user)
        session.commit()
        session.refresh(user)
        return {"id": user.id, "username": user.username, "role": user.role}

@app.get("/incidents", response_model=List[Incident])
def list_incidents(current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        incidents = session.exec(select(Incident)).all()
        return incidents

@app.post("/incidents", status_code=201, response_model=Incident)
def create_incident(i: IncidentCreate, current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        incident = Incident(title=i.title, description=i.description, created_by=current_user.id)
        session.add(incident)
        session.commit()
        session.refresh(incident)
        return incident
