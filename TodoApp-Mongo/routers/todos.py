import sys
sys.path.append("..")

from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from pydantic import BaseModel, Field

from typing import Optional

from database import engine, SessionLocal, conn
from sqlalchemy.orm import Session

import models
from database import serializeDict, serializeList
from .auth import get_current_user, get_user_exception


router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={
        404: {"detail": "Not Found"}
    }
)

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class Todo(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(ge=1, le=5)
    complete: bool



 
@router.get('/')
async def read_all(db: Session = Depends(get_db)):
    print('**********************')
    print(conn.blog.posts.find())
    return serializeList(conn.blog.posts.find())
    return db.query(models.Todos).all()


@router.get('/user')
async def read_all_by_user(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()  

    return db.query(models.Todos).filter(models.Todos.owner_id == user.get("user_id")).all()


@router.get('/{todo_id}')
async def read_todo(todo_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    
    todo_model = db.query(models.Todos)\
        .filter(models.Todos.id == todo_id)\
        .filter(models.Todos.owner_id == user["user_id"])\
        .first()
    if todo_model is not None: 
        return todo_model
    raise HTTPException_todo_notfound()


@router.put('/{todo_id}')
async def update_todo(todo_id: int, todo: Todo, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id)\
        .filter(models.Todos.owner_id == user["user_id"])\
        .first()
    
    if todo_model is not None:
        todo_model.title = todo.title
        todo_model.description = todo.description
        todo_model.priority = todo.priority
        todo_model.complete = todo.complete

        db.add(todo_model)
        db.commit()

        return {
            'status': 200,
            'detail': 'updated'
        }
    
    raise HTTPException_todo_notfound()


@router.delete('/{todo_id}')
async def delete_todo(todo_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id)\
        .filter(models.Todos.owner_id == user["user_id"])\
        .first()
    
    if todo_model is not None:
        db.query(models.Todos).filter(models.Todos.id == todo_id).delete()
        db.commit()
        
        return {
            'status': 201,
            'detail': 'deleted'
        }
    
    raise HTTPException_todo_notfound()


@router.post('/')
async def create_todo(todo: Todo, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    
    todo_model = models.Todos()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    todo_model.owner_id = user.get("user_id")

    db.add(todo_model)
    db.commit()

    return {
        'status': 201,
        'detail': 'created'
    }



def HTTPException_todo_notfound():
    return HTTPException(status_code=404, detail="Todo Not Found")