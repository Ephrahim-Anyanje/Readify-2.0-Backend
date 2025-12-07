# routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import crud
import schemas

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=schemas.UserOut)
def create_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user(db, user_in.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    return crud.create_user(
        db,
        user_in.username,
        user_in.email,
        user_in.password
    )

@router.get("/{username}", response_model=schemas.UserOut)
def get_user(username: str, db: Session = Depends(get_db)):
    u = crud.get_user(db, username)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    return u
