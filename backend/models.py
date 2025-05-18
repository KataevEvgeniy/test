from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base, engine


class User(Base):
    """Модель пользователя"""
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=True)
    password = Column(String, nullable=True)

    books = relationship("UserBook", back_populates="user")  # Связь с книгами


class Book(Base):
    """Модель книги"""
    __tablename__ = "book"

    book_id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String, nullable=True)  # Путь к файлу книги
    file_type = Column(String, nullable=True)  # Формат файла (pdf, epub и т.д.)
    author = Column(String, nullable=True)
    image_path = Column(String, nullable=True)  # Путь к изображению (обложка книги)
    title = Column(String, nullable=True)
    count_pages = Column(Integer, nullable=True)

    users = relationship("UserBook", back_populates="book")  # Связь с пользователями


class UserBook(Base):
    """Связь пользователя и книги"""
    __tablename__ = "user_book"

    user_id = Column(Integer, ForeignKey("user.user_id"), primary_key=True)
    book_id = Column(Integer, ForeignKey("book.book_id"), primary_key=True)
    current_page = Column(Integer, nullable=True)  # Текущая страница чтения
    last_open_date = Column(Integer, nullable=True)  # Дата последнего открытия

    user = relationship("User", back_populates="books")
    book = relationship("Book", back_populates="users")


# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)

