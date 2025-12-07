# routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import crud
import schemas
from models import User

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user account
    """
    # Check if username already exists
    existing = crud.get_user_by_username(db, user_in.username)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    # Check if email already exists (if provided)
    if user_in.email:
        existing_email = crud.get_user_by_email(db, user_in.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )

    # Create the user
    return crud.create_user(
        db,
        username=user_in.username,
        email=user_in.email,
        password=user_in.password,
        full_name=user_in.full_name
    )


@router.get("/me", response_model=schemas.UserOut)
def get_current_user(db: Session = Depends(get_db)):
    """
    Get currently authenticated user
    
    This is a placeholder - implement proper JWT token validation here
    """
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated"
    )


@router.get("/{username}", response_model=schemas.UserOut)
def get_user(username: str, db: Session = Depends(get_db)):
    """
    Get user by username
    """
    user = crud.get_user_by_username(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.put("/{user_id}", response_model=schemas.UserOut)
def update_user(
    user_id: int, 
    user_update: schemas.UserUpdate,
    db: Session = Depends(get_db)
):
    """
    Update user information
    """
    user = crud.update_user(db, user_id, user_update.full_name)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.get("/", response_model=list[schemas.UserOut])
def list_users(db: Session = Depends(get_db)):
    """
    List all users (for admin purposes)
    """
    return crud.get_all_users(db)