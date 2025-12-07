# crud.py
from typing import Optional
from sqlalchemy.orm import Session
from models import User, Book, Activity
from schemas import UserCreate, BookCreate
from passlib.context import CryptContext

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a plain text password"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain text password against a hashed password"""
    return pwd_context.verify(plain_password, hashed_password)


# ============================================================================
# USER CRUD OPERATIONS
# ============================================================================

def create_user(
    db: Session, 
    username: str, 
    email: Optional[str], 
    password: str, 
    full_name: Optional[str] = None
) -> User:
    """Create a new user with hashed password"""
    password_hash = hash_password(password)
    new_user = User(
        username=username,
        email=email,
        password_hash=password_hash,
        full_name=full_name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Get user by username"""
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()


def get_user(db: Session, username: str) -> Optional[User]:
    """Alias for get_user_by_username"""
    return get_user_by_username(db, username)


def get_all_users(db: Session):
    """Get all users"""
    return db.query(User).all()


def update_user(db: Session, user_id: int, full_name: Optional[str] = None) -> Optional[User]:
    """Update user information"""
    user = get_user_by_id(db, user_id)
    if user:
        if full_name is not None:
            user.full_name = full_name
        db.commit()
        db.refresh(user)
    return user


# ============================================================================
# BOOK CRUD OPERATIONS
# ============================================================================

def create_book(db: Session, book: BookCreate, owner_id: int = None) -> Book:
    """Create a new book"""
    new_book = Book(
        title=book.title,
        author=book.author,
        description=book.description
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


def get_book(db: Session, book_id: int) -> Optional[Book]:
    """Get book by ID"""
    return db.query(Book).filter(Book.id == book_id).first()


def get_book_by_google_id(db: Session, google_id: str) -> Optional[Book]:
    """Get book by Google Books ID"""
    return db.query(Book).filter(Book.external_id == google_id).first()


def get_books_for_user(db: Session, user_id: int):
    """Get all books associated with a user through activities"""
    return (
        db.query(Book)
        .join(Activity)
        .filter(Activity.user_id == user_id)
        .all()
    )


def list_books(db: Session):
    """Get all books"""
    return db.query(Book).all()


# ============================================================================
# ACTIVITY CRUD OPERATIONS
# ============================================================================

def create_activity(
    db: Session, 
    user: User, 
    book: Book, 
    status: str, 
    progress: int = 0
) -> Activity:
    """Create a new reading activity"""
    new_activity = Activity(
        user_id=user.id,
        book_id=book.id,
        status=status,
        progress=progress
    )
    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)
    return new_activity


def get_user_activities(db: Session, user: User):
    """Get all activities for a user"""
    return db.query(Activity).filter(Activity.user_id == user.id).all()


def get_user_activity(db: Session, user_id: int):
    """Get all activities for a user by user_id"""
    return db.query(Activity).filter(Activity.user_id == user_id).all()


def update_activity(
    db: Session, 
    activity_id: int, 
    status: Optional[str] = None, 
    progress: Optional[int] = None
) -> Optional[Activity]:
    """Update an activity"""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if activity:
        if status is not None:
            activity.status = status
        if progress is not None:
            activity.progress = progress
        db.commit()
        db.refresh(activity)
    return activity