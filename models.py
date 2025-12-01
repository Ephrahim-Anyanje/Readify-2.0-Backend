# models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(128), unique=True, index=True, nullable=False)
    email = Column(String(256), unique=True, index=True, nullable=True)
    activities = relationship("ReadingActivity", back_populates="user", cascade="all, delete-orphan")

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(512), nullable=False)
    author = Column(String(256), nullable=True)
    description = Column(Text, nullable=True)
    cover_image = Column(String(512), nullable=True)
    category = Column(String(128), nullable=True)
    external_id = Column(String(128), unique=True, nullable=True, index=True)
    activities = relationship("ReadingActivity", back_populates="book", cascade="all, delete-orphan")

class ReadingActivity(Base):
    __tablename__ = "reading_activity"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    status = Column(String(64), nullable=False, default="wishlist")  # favorite, reading, completed, wishlist
    progress = Column(Integer, nullable=True, default=0)
    date_added = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="activities")
    book = relationship("Book", back_populates="activities")
