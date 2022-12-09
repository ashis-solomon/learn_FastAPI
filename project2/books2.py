from fastapi import FastAPI
from pydantic import BaseModel, Field

from typing import Optional
from uuid import UUID

app = FastAPI()


class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(min_length=1, max_length=100)
    rating: int = Field(ge=0, le=100)

    class Config:
        schema_extra = {
            "example": {
                "id": "0526f5e7-3246-4a8c-801f-d426e708ac1e",
                "title": "title1",
                "author": "author1",
                "description": "desc1",
                "rating": 1
            }
        }



BOOKS = []


@app.get('/')
async def read_all_books(limit: Optional[int] = None):
    BOOKS_copy = []
    if limit:
        i=0
        for x in BOOKS:
            i+=1
            BOOKS_copy.append(x)
            if i == limit:
                break
        print(BOOKS_copy)
        return BOOKS_copy

    return BOOKS

@app.get('/book/{book_id}')
async def read_book(book_id: UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x
    return {'detail': 'Book not Found'}

@app.post('/')
async def create_book(book: Book):
    BOOKS.append(book)
    return book

@app.put('/{book_id}')
async def update_book(book_id: UUID, book: Book):
    counter = 0
    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            BOOKS[counter-1] = book
            return book
    return {'detail': 'Book not Found'}

@app.delete('/{book_id}')
async def delete_book(book_id: UUID):
    counter = 0
    for x in BOOKS:
        counter += 1
        if x.id == book_id:          
            return BOOKS.pop(counter-1)
    return {'detail': 'Book not Found'}



def create_books_no_api():
    book1 = Book(
        id = "0526f5e7-3246-4a8c-801f-d426e708ac1e",
        title = "title1",
        author= "author1",
        description= "desc1",
        rating = 1
    )

    book2 = Book(
        id = "77c3e007-a2c4-4df1-a624-f6966d216d70",
        title = "title2",
        author= "author2",
        description= "desc2",
        rating = 2
    )
    
    book3 = Book(
        id = "b87a94d0-e3e8-40da-87a7-23d8110616b4",
        title = "title3",
        author= "author3",
        description= "desc3",
        rating = 3
    )

    book4 = Book(
        id = "9b048731-96d9-499c-8c18-ff17d1d0358f",
        title = "title4",
        author= "author4",
        description= "desc4",
        rating = 4
    )

    BOOKS.append(book1)
    BOOKS.append(book2)
    BOOKS.append(book3)
    BOOKS.append(book4)

# creating dummy books
create_books_no_api()
