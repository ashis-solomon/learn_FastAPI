import sys
sys.path.append("..")

from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from pydantic import BaseModel, Field

from typing import Optional

from database import engine, SessionLocal
from sqlalchemy.orm import Session

import bcrypt
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
import jwt

import models


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses= {
        401: {"user": "Not Authorized"}
    }
)

# For JWT Generation
SECRET_KEY = "4ac42adc-8ab6-4610-a5be-e832ffce714c"
ALGORIHTM = "HS256"

outh2_bearer = OAuth2PasswordBearer(tokenUrl="token")


models.Base.metadata.create_all(bind=engine)

class CreateUser(BaseModel):
    username: str
    email: Optional[str]
    firstname: str
    lastname: str
    password: str

class LoginUser(BaseModel):
    username: str
    password: str

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_password_hash(password):
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash

def verify_password(plain_password, hash):
    userBytes = plain_password.encode('utf-8')
    result = bcrypt.checkpw(userBytes, hash)
    return result

def authenticate_user(username: str, password: str, db):
    user = db.query(models.Users).filter(models.Users.username == username).first()
    if not user:
        return False

    if verify_password(password, user.hashed_password):
        return user
    return False

def create_access_token(username: str, user_id: int, expires_delta: Optional[timedelta] = None):
    encode = {
        "sub": username,
        "id": user_id
    }
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({"exp": expire})

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORIHTM)


@router.post('/login/v1')
async def login(login_user: LoginUser, db: Session = Depends(get_db)):
    user = authenticate_user(login_user.username, login_user.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="validation failure")
    token = create_access_token(user.username, user.id, expires_delta=timedelta(minutes=30))
    return {
        'token': token
    }

@router.post('/create/user')
async def create_new_user(create_user: CreateUser, db: Session = Depends(get_db)):
    create_user_model = models.Users()
    create_user_model.email = create_user.email
    create_user_model.username = create_user.username
    create_user_model.firstname = create_user.firstname
    create_user_model.lastname = create_user.lastname
    create_user_model.hashed_password = get_password_hash(create_user.password)
    create_user_model.is_active = True

    db.add(create_user_model)
    db.commit()

    return {
        'status': status.HTTP_200_OK,
        'detail': 'created'
    }

# Generate JWT Tokens
@router.post('/token')
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise token_exception()

    token_expires = timedelta(minutes=20)
    token = create_access_token(user.username, user.id, expires_delta=token_expires)

    return {
        "token": token
    }


async def get_current_user(token: str = Depends(outh2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORIHTM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")

        if username is None or user_id is None:
            raise get_user_exception()
        
        return {
            "username": username,
            "user_id": user_id
        }
    except:
        raise get_user_exception()


# Exceptions
def get_user_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

def token_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect Username or Password",
        headers={"WWW-Authenticate": "Bearer"}
    )