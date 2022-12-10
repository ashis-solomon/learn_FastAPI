from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import bcrypt

import models


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

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

def authenticate_user(password, hash):
    userBytes = password.encode('utf-8')
    result = bcrypt.checkpw(userBytes, hash)
    return result

class CreateUser(BaseModel):
    username: str
    email: Optional[str]
    firstname: str
    lastname: str
    password: str


@app.post('/create/user')
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
        'status': 200,
        'detail': 'created'
    }
