import os
from typing import Optional

from sqlalchemy.orm import Session
from models import Book, UserBook
from schemas import BookCreate, UserBookData
from datetime import datetime

UPLOAD_DIR = "books"
IMAGE_DIR = "images"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)

def create_book(db: Session, book: BookCreate):
    """Создаёт новую книгу с проверкой на существование книги с таким же названием и автором"""

    # Проверяем, существует ли уже книга с таким же автором и названием
    existing_book = db.query(Book).filter(
        Book.author == book.author,
        Book.title == book.title
    ).first()

    if existing_book:
        # Если книга уже существует, выбрасываем ошибку
        raise ValueError(f"Книга с названием '{book.title}' и автором '{book.author}' уже существует.")

    # Путь к файлам книги и изображения
    file_path = os.path.join(UPLOAD_DIR, f"{(book.author + ' ' + book.title).replace(' ', '_')}.{book.fileType}")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(book.file)

    image_path = os.path.join(IMAGE_DIR, f"{(book.author + ' ' + book.title).replace(' ', '_')}")
    with open(image_path, "w", encoding="utf-8") as img_file:
        img_file.write(book.image)

    # Создаём новую книгу в базе данных
    new_book = Book(
        title=book.title,
        author=book.author,
        file_path=file_path,
        file_type=book.fileType,
        count_pages=book.countPages,
        image_path=image_path
    )

    # Добавляем книгу в базу данных
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book

def save_user_book_data(db: Session, user_book_data: UserBookData):
    """Сохраняет или обновляет прогресс чтения книги пользователем"""

    user_book = db.query(UserBook).filter_by(
        user_id=user_book_data.userId,
        book_id=user_book_data.bookId
    ).first()

    if user_book:
        user_book.current_page = user_book_data.currentPage
        user_book.last_open_date = user_book_data.lastOpenDate
    else:
        user_book = UserBook(
            user_id=user_book_data.userId,
            book_id=user_book_data.bookId,
            current_page=user_book_data.currentPage,
            last_open_date=user_book_data.lastOpenDate
        )
        db.add(user_book)

    db.commit()
    return user_book

def get_book_by_id(db: Session, book_id: int):
    """Получает книгу по ID и возвращает содержимое файлов"""
    book = db.query(Book).filter(Book.book_id == book_id).first()
    if book:
        # Читаем файл книги
        with open(book.file_path, 'r', encoding='utf-8') as file:
            book_content = file.read()

        # Читаем изображение
        with open(book.image_path, 'r', encoding='utf-8') as img_file:
            book_image = img_file.read()

        # Возвращаем книгу с содержимым файлов
        return {
            "bookId": book.book_id,
            "title": book.title,
            "author": book.author,
            "countPages": book.count_pages,
            "fileType": book.file_type,
            "file": book_content,  # Содержимое файла книги
            "image": book_image  # Содержимое изображения
        }
    return None

def get_all_books(db: Session):
    """Получает все книги (без загрузки файлов)"""
    books = db.query(Book).all()
    result = []
    for book in books:
        # Не загружаем содержимое файлов здесь, только информацию о книге
        result.append({
            "book_id": book.book_id,
            "title": book.title,
            "author": book.author,
            "count_pages": book.count_pages,
            "image_path": book.image_path  # Возвращаем путь изображения, но не сам файл
        })
    return result

def get_user_book_data(db: Session, user_id: int, book_id: int):
    """Получает данные о прогрессе чтения книги пользователем"""
    user_book = db.query(UserBook).filter(UserBook.user_id == user_id, UserBook.book_id == book_id).first()
    if user_book:
        return {
            "user_id": user_book.user_id,
            "book_id": user_book.book_id,
            "current_page": user_book.current_page,
            "last_open_date": user_book.last_open_date
        }
    return None
