import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from crud import create_book, get_book_by_id, save_user_book_data, get_all_books, get_user_book_data
from database import get_db
from typing import List, Optional

from schemas import BookResponse, BookCreate, UserBookData

app = FastAPI(title="📚 Читалка книг API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.post("/books/")
def add_book(book: BookCreate, db: Session = Depends(get_db)):
    """Создать новую книгу"""
    try:
        created_book = create_book(db, book)
        return {"message": "Book created successfully", "book_id": created_book.book_id}
    except ValueError as e:
        # Обрабатываем ошибку, если книга уже существует
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/books-data/")
def add_user_book_data(data: UserBookData, db: Session = Depends(get_db)):
    """Создать новую книгу"""
    save_user_book_data(db, data)
    return "success"

@app.get("/user-books/{user_id}/{book_id}")
def get_user_book_progress(user_id: int, book_id: int, db: Session = Depends(get_db)):
    """Получает данные о прогрессе чтения книги пользователем"""
    user_book_data = get_user_book_data(db, user_id, book_id)
    if user_book_data is None:
        raise HTTPException(status_code=404, detail="User progress not found")
    return user_book_data

@app.get("/books/{book_id}")
def get_book(book_id: int, db: Session = Depends(get_db)):
    """Получает книгу по ID с содержимым файлов"""
    book = get_book_by_id(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.get("/books/", response_model=List[BookResponse])
def get_books(db: Session = Depends(get_db)):
    """Получает список всех книг (без содержимого файлов)"""
    books = get_all_books(db)
    return books

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)