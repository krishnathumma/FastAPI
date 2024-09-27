from typing import Optional

from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not Needed for Create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=5)
    description: str = Field(min_length=5, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1980, lt=2035)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new Book",
                "author": "Humans",
                "description": "A book of books",
                "rating": 4,
                "published_date": 2012
            }
        }
    }


BOOKS = [
    Book(1, 'Telugu', 'Pandit', 'Reginal Book', 6, 2012),
    Book(2, 'Maths', 'Devi', 'Good Book!', 5, 2022),
    Book(6, 'Physics', "Roy", "Super Copy!", 5, 2015),
    Book(3, 'CS', "Tyoler", "Nice Book!", 5, 2002),
    Book(4, 'Social', "All", "OK Ok Book!", 2, 2024),
    Book(5, 'English', "MAxwell", "Book Book!", 5, 2000),
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not Found")


@app.get("/books/", status_code=status.HTTP_200_OK)
async def get_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    result_book = []
    for book in BOOKS:
        if book.rating == book_rating:
            result_book.append(book)

    return result_book


@app.post("/books/create_book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.dict())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    # if len(BOOKS) > 0:
    #     book.id = BOOKS[-1].id + 1
    # else:
    #     book.id = 1

    return book


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_updated = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_updated = True
    if not book_updated:
        raise HTTPException(status_code=404, detail="Book Not Found")


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_deleted = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_deleted = True
            break
    if not book_deleted:
        raise HTTPException(status_code=404, detail="Book Not Found")


@app.get("/books/publish",status_code=status.HTTP_200_OK)
async def book_by_year(published_date: int = Query(gt=1980, lt=2035)):
    result_book = []
    for book in BOOKS:
        if book.published_date == published_date:
            result_book.append(book)
    return result_book
