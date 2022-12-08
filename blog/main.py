from fastapi import FastAPI, Depends, Response, status

from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def index():
    return "Index"

@app.post("/blog", status_code=status.HTTP_201_CREATED)
async def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get("/blog/all")
async def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get("/blog/{id}")
async def get_blog_id(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": f"blog with {id} not found"}
    return blog