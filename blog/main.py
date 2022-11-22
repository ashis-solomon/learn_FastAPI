from fastapi import FastAPI

from . import schemas, models
from .database import engine


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/")
async def index():
    return "Index"

@app.post("/blog")
async def create_blog(request: schemas.Blog):
    return request