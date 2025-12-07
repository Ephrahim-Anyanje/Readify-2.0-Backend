# schemas.py
from pydantic import BaseModel
from typing import Optional

# User
class UserCreate(BaseModel):
    username: str
    email: Optional[str] = None

class UserOut(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    class Config:
        orm_mode = True

# Book
class BookBase(BaseModel):
    title: str
    author: Optional[str] = None
    description: Optional[str] = None
    cover_image: Optional[str] = None
    category: Optional[str] = None
    external_id: Optional[str] = None

class BookCreate(BaseModel):
    title: str
    author: str
    description: str = None


class BookOut(BookBase):
    id: int
    class Config:
        orm_mode = True

# Activity
class ActivityCreate(BaseModel):
    username: str
    book_id: int
    status: str
    progress: int = 0

class ActivityOut(BaseModel):
    id: int
    status: str
    progress: int
    book: BookOut
    class Config:
        orm_mode = True
