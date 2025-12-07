from typing import Optional
from sqlalchemy.orm import Session
from models import User, Book, Activity
from schemas import UserCreate, BookCreate


# USER CRUD
def create_user(db: Session, user: UserCreate):
    new_user = User(
        username=user.username,
        email=user.email
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_all_users(db: Session):
    return db.query(User).all()

# BOOK CRUD
def create_book(db: Session, book: BookCreate, owner_id: int):
    new_book = Book(
        title=book.title,
        author=book.author,
        google_id=book.google_id,
        owner_id=owner_id
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


def get_book_by_google_id(db: Session, google_id: str):
    return db.query(Book).filter(Book.google_id == google_id).first()


def get_books_for_user(db: Session, user_id: int):
    return db.query(Book).filter(Book.owner_id == user_id).all()


# ACTIVITY CRUD
def log_activity(db: Session, user_id: int, action: str, book_title: Optional[str] = None):
    new_activity = Activity(
        user_id=user_id,
        action=action,
        book_title=book_title,
    )
    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)
    return new_activity


def get_user_activity(db: Session, user_id: int):
    return db.query(Activity).filter(Activity.user_id == user_id).all()
