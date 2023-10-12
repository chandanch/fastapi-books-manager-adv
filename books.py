"""
Books API
"""
from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    """
    Book class
    """

    book_id: int
    title: str
    author: str
    category: str
    rating: int

    def __init__(self, book_id, title, author, category, rating):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.category = category
        self.rating = rating


class BookRequest(BaseModel):
    """
    BookRequest model
    """

    book_id: Optional[int] = Field(
        default=None, title="book_id is optional and will be ignored"
    )
    title: str = Field(min_length=4, max_length=100)
    author: str = Field(min_length=2, max_length=10)
    category: str = Field(min_length=3)
    rating: int = Field(gt=0, lt=6)

    class Config:
        """
        schema config
        """

        json_schema_extra = {
            "example": {
                "title": "My new Birnds",
                "author": "chandanch",
                "category": "lean",
                "rating": 4,
            }
        }


BOOKS = [
    Book(1, "Programming with Py", "chandanch", "computers", 4),
    Book(2, "Programming with TS", "fameer", "computers", 3),
    Book(3, "Divine", "chandanch", "spiritual", 4),
    Book(4, "Programming with R", "chandanch", "computers", 5),
]


@app.get("/books")
async def get_books():
    """
    Returns all books
    """
    return BOOKS


@app.get("/books/search")
# use Query() to validate query params
async def search_books(rating: int = Query(gt=0, lt=6)):
    """
    Search all books
    """
    books_results = []
    for book in BOOKS:
        if book.rating == rating:
            books_results.append(book)

    return books_results


@app.post("/books")
async def create_book(book: BookRequest):
    """
    Add new book
    """
    new_book = Book(**book.model_dump())
    BOOKS.append(generate_id(new_book))
    return new_book


def generate_id(book):
    """
    increment ID
    """
    book.book_id = 1 if len(BOOKS) == 0 else BOOKS[-1].book_id + 1
    return book


@app.get("/books/{book_id}")
# Path() is used to validate a specific path parameter
# here we are enforcing that book_id must be > 0
async def get_book_by_id(book_id: int = Path(gt=0)):
    """
    Get Book by ID
    """
    for book in BOOKS:
        if book.book_id == book_id:
            return book
    raise HTTPException(
        status_code=404,
        detail={
            "error": "Book not found",
            "msg": f"Book with ID: {book_id} not found",
        },
    )


@app.put("/books/{book_id}")
async def update_book(book: BookRequest, book_id: int = Path(gt=0)):
    """
    update book
    """
    for i, book in enumerate(BOOKS):
        if BOOKS[i].book_id == book_id:
            BOOKS[i] = book
            return {"status": "success"}
    return {"stauts": "Not found"}
