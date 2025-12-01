from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, nullable=True)

    activities = relationship("ReadingActivity", back_populates="user")


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    description = Column(Text)
    cover_image = Column(String)
    category = Column(String)
    external_id = Column(String, unique=True)


class ReadingActivity(Base):
    __tablename__ = "reading_activity"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    status = Column(String)
    progress = Column(Integer)
    date_added = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="activities")
    book = relationship("Book")
