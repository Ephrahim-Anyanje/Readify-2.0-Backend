# routers/activity.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import crud
import schemas

router = APIRouter(prefix="/activity", tags=["activity"])


@router.get("/recent", response_model=List[schemas.ActivityOut])
def get_recent_activity(limit: int = 10, db: Session = Depends(get_db)):
    """
    Get recent activity across all users (for dashboard)
    """
    from models import Activity
    activities = db.query(Activity).order_by(
        Activity.date_added.desc()
    ).limit(limit).all()
    # Convert is_favorite to bool for all activities
    for activity in activities:
        activity.is_favorite = bool(activity.is_favorite)
    return activities


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
    
    # Check if activity already exists
    from models import Activity
    existing = db.query(Activity).filter(
        Activity.user_id == user.id,
        Activity.book_id == book.id
    ).first()
    
    if existing:
        # Return existing activity instead of creating duplicate
        # Convert is_favorite to bool for response
        existing.is_favorite = bool(existing.is_favorite)
        return existing
    
    # Create activity
    activity = crud.create_activity(db, user, book, data.status, data.progress)
    # Convert is_favorite to bool for response
    activity.is_favorite = bool(activity.is_favorite)
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
    activities = crud.get_user_activities(db, user)
    # Convert is_favorite to bool for all activities
    for activity in activities:
        activity.is_favorite = bool(activity.is_favorite)
    return activities


@router.get("/book/{book_id}/user/{username}", response_model=schemas.ActivityOut)
def get_book_activity(book_id: int, username: str, db: Session = Depends(get_db)):
    """
    Get activity for a specific book and user
    """
    user = crud.get_user(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    activity = crud.get_activity_by_book_and_user(db, book_id, user.id)
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found for this book"
        )
    # Convert is_favorite to bool
    activity.is_favorite = bool(activity.is_favorite)
    return activity


@router.put("/{activity_id}", response_model=schemas.ActivityOut)
def update_activity(
    activity_id: int,
    update_data: schemas.ActivityUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an activity (progress, status, favorite)
    """
    activity = crud.update_activity(
        db,
        activity_id,
        status=update_data.status,
        progress=update_data.progress,
        is_favorite=update_data.is_favorite
    )
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Convert is_favorite to bool
    activity.is_favorite = bool(activity.is_favorite)
    return activity


@router.delete("/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_activity(activity_id: int, db: Session = Depends(get_db)):
    """
    Remove a book from user's library (delete activity)
    """
    from models import Activity
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    db.delete(activity)
    db.commit()
    return None