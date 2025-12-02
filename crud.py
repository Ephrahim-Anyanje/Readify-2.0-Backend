# crud.py
from sqlalchemy.orm import Session
import models

# USERS
def create_user(db: Session, username: str, email: str | None = None):
    user = models.User(username=username, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

# BOOKS
def get_book_by_external_id(db: Session, external_id: str):
    return db.query(models.Book).filter(models.Book.external_id == external_id).first()

def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_or_create_book(db: Session, data: dict):
    if data.get("external_id"):
        existing = get_book_by_external_id(db, data["external_id"])
        if existing:
            return existing
    book = models.Book(
        title=data.get("title"),
        author=data.get("author"),
        description=data.get("description"),
        cover_image=data.get("cover_image"),
        category=data.get("category"),
        external_id=data.get("external_id")
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

def list_books(db: Session):
    return db.query(models.Book).order_by(models.Book.title).all()

# ACTIVITY
def create_activity(db: Session, user: models.User, book: models.Book, status: str, progress: int = 0):
    act = models.ReadingActivity(user_id=user.id, book_id=book.id, status=status, progress=progress)
    db.add(act)
    db.commit()
    db.refresh(act)
    return act

def get_user_activities(db: Session, user: models.User):
    return db.query(models.ReadingActivity).filter(models.ReadingActivity.user_id == user.id).all()

def update_activity(db: Session, activity_id: int, status: str | None = None, progress: int | None = None):
    act = db.query(models.ReadingActivity).filter(models.ReadingActivity.id == activity_id).first()
    if not act:
        return None
    if status:
        act.status = status
    if progress is not None:
        act.progress = progress
    db.commit()
    db.refresh(act)
    return act
