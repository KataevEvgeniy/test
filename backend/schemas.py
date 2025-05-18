from fastapi import UploadFile
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBookData(BaseModel):
    """Схема данных о пользователе и книге"""
    userId: int
    bookId: int
    currentPage: Optional[int] = None
    lastOpenDate: Optional[int] = None

class BookCreate(BaseModel):
    file: str  # Путь к файлу
    fileType: str
    author: str
    title: str
    image: Optional[str] = None
    countPages: Optional[int] = None


class BookResponse(BaseModel):
    book_id: int
    title: str
    author: str
    count_pages: Optional[int] = None
    image_path: Optional[str] = None

