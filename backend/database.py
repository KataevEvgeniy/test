from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///books.db"

# Создаем движок для работы с SQLite
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Создаем базовый класс для моделей
Base = declarative_base()

# Создаем сессию для работы с БД
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    """Функция для создания сессии"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
