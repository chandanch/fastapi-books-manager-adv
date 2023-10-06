from fastapi import FastAPI

app = FastAPI()

BOOKS = [{"name": "dedewd", "active": False}]


@app.get("/books")
async def get_books():
    return BOOKS
