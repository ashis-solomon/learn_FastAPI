from typing import Optional
from fastapi import FastAPI
from enum import Enum

app = FastAPI()


BOOKS = {
    'book_1': {'title': 'Title One', 'author': 'Author One'},
    'book_2': {'title': 'Title Two', 'author': 'Author Two'},
    'book_3': {'title': 'Title Three', 'author': 'Author Three'},
    'book_4': {'title': 'Title Four', 'author': 'Author Four'},
    'book_5': {'title': 'Title Five', 'author': 'Author Five'},
}

class DirectionName(Enum):
    north = "North"
    south = "South"
    east = "East"
    west = "West"


@app.get('/')
async def read_all_books(skip_book: Optional[str] = None):
    if skip_book:
        new_books = BOOKS.copy()
        try:
            new_books.pop(skip_book)
        except:
            pass
        return new_books
    return BOOKS


@app.get('/{book_name}')
async def read_book(book_name: str):
    try:
        return BOOKS[book_name]
    except:
        return {"detail": "Book not Found"}


@app.post('/{book_name}')
async def create_book(book_title: str, book_author: str):
    book = {'title': book_title, 'author': book_author}
    BOOKS[f'book_{len(BOOKS)+1}'] = book
    return {'detail': 'created'}


@app.put('/{book_name}')
async def update_specific_book(book_name: str, book_title: str, book_author: str):
    book = {
        'title': book_title,
        'author': book_author
    }
    BOOKS[book_name] = book
    return {'detail': 'updated'}


@app.delete('/{book_name}')
async def delete_specific_book(book_name: str):
    try:
        book = BOOKS.pop(book_name)
    except:
        return {'detail': 'Book not Found'}
    return {'detail': f'{book_name} : {book} deleted'}