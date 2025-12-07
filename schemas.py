# schemas.py
from pydantic import BaseModel
from typing import Optional

# User
class UserCreate(BaseModel):
    username: str
    email: Optional[str] = None
    password: str
    full_name: Optional[str] = None

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class UserOut(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    
    class Config:
        from_attributes = True  # Updated from orm_mode in Pydantic v2

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
    author: Optional[str] = None
    description: Optional[str] = None
    cover_image: Optional[str] = None
    category: Optional[str] = None
    external_id: Optional[str] = None

class BookOut(BookBase):
    id: int
    
    class Config:
        from_attributes = True

# Activity
class ActivityCreate(BaseModel):
    username: str
    book_id: int
    status: str
    progress: int = 0

class ActivityUpdate(BaseModel):
    status: Optional[str] = None
    progress: Optional[int] = None
    is_favorite: Optional[bool] = None

class ActivityOut(BaseModel):
    id: int
    status: str
    progress: int
    is_favorite: bool = False
    book: BookOut
    
    class Config:
        from_attributes = True