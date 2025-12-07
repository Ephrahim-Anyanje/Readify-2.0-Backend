# routers/activity.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import crud
import schemas

router = APIRouter(prefix="/activity", tags=["activity"])

@router.post("/", response_model=schemas.ActivityOut)
def create_activity(data: schemas.ActivityCreate, db: Session = Depends(get_db)):
    user = crud.get_user(db, data.username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    book = crud.get_book(db, data.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    act = crud.create_activity(db, user, book, data.status, data.progress)
    return act

@router.get("/{username}", response_model=List[schemas.ActivityOut])
def get_user_library(username: str, db: Session = Depends(get_db)):
    user = crud.get_user(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.get_user_activities(db, user)
