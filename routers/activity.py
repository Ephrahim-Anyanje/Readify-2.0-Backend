# routers/activity.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import crud
import schemas

router = APIRouter(prefix="/activity", tags=["activity"])


@router.post("/", response_model=schemas.ActivityOut, status_code=status.HTTP_201_CREATED)
def create_activity(data: schemas.ActivityCreate, db: Session = Depends(get_db)):
    """
    Create a new reading activity for a user
    """
    # Get user
    user = crud.get_user(db, data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get book
    book = crud.get_book(db, data.book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    # Create activity
    activity = crud.create_activity(db, user, book, data.status, data.progress)
    return activity


@router.get("/{username}", response_model=List[schemas.ActivityOut])
def get_user_library(username: str, db: Session = Depends(get_db)):
    """
    Get all reading activities (library) for a specific user
    """
    user = crud.get_user(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return crud.get_user_activities(db, user)


@router.get("/recent", response_model=List[schemas.ActivityOut])
def get_recent_activity(limit: int = 10, db: Session = Depends(get_db)):
    """
    Get recent activity across all users (for dashboard)
    """
    activities = db.query(crud.Activity).order_by(
        crud.Activity.date_added.desc()
    ).limit(limit).all()
    return activities