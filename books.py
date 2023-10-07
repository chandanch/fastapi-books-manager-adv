from fastapi import Body, FastAPI

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


BOOKS = [
    Book(1, "Programming with Py", "chandanch", "computers", 4),
    Book(2, "Programming with TS", "fameer", "computers", 3),
    Book(3, "Divine", "chandanch", "spiritual", 4),
    Book(1, "Programming with R", "chandanch", "computers", 5),
]


@app.get("/books")
async def get_books():
    """
    Returns all books
    """
    return BOOKS


@app.post("/books")
async def create_book(book=Body()):
    """
    Add new book
    """
    BOOKS.append(book)
