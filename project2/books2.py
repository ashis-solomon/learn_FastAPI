from fastapi import FastAPI
from pydantic import BaseModel, Field

from typing import Optional
from uuid import UUID

app = FastAPI()


class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str
    description: Optional[str] = Field(min_length=1, max_length=100)
    rating: int


BOOKS = []


@app.get('/')
async def read_all_books():
    return BOOKS

@app.post('/')
async def create_book(book: Book):
    BOOKS.append(book)
    return book