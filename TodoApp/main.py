from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, Field

from typing import Optional

from database import engine, SessionLocal
from sqlalchemy.orm import Session

import models
from auth import get_current_user, get_user_exception



app = FastAPI()

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


 
@app.get('/')
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Todos).all()


@app.get('/todos/user')
async def read_all_by_user(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    return db.query(models.Todos).filter(models.Todos.owner_id == user.get("user_id")).all()


@app.get('/todo/{todo_id}')
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


@app.put('/todo/{todo_id')
async def update_todo(todo_id: int, todo: Todo, db: Session = Depends(get_db)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    
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


@app.delete('/todo/{todo_id')
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    
    if todo_model is not None:
        db.query(models.Todos).filter(models.Todos.id == todo_id).delete()
        db.commit()
        
        return {
            'status': 201,
            'detail': 'deleted'
        }
    
    raise HTTPException_todo_notfound()


@app.post('/')
async def create_todo(todo: Todo, db: Session = Depends(get_db)):
    todo_model = models.Todos()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete

    db.add(todo_model)
    db.commit()

    return {
        'status': 201,
        'detail': 'created'
    }



def HTTPException_todo_notfound():
    return HTTPException(status_code=404, detail="Todo Not Found")