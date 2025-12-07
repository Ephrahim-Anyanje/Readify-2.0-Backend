# routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import crud
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["authentication"])


class TokenRequest(BaseModel):
    """Login credentials"""
    username: str
    password: str


class TokenResponse(BaseModel):
    """Authentication token response"""
    access_token: str
    token_type: str = "bearer"


@router.post("/token", response_model=TokenResponse)
def login(credentials: TokenRequest, db: Session = Depends(get_db)):
    """
    Authenticate user and return access token
    
    For now, this returns a simple token. In production, use JWT tokens.
    """
    # Get user by username
    user = crud.get_user_by_username(db, credentials.username)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not crud.verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Return token (simplified - in production use JWT)
    return TokenResponse(
        access_token=f"user_{user.id}_{user.username}",
        token_type="bearer"
    )


@router.post("/signup", response_model=TokenResponse)
def signup(credentials: TokenRequest, db: Session = Depends(get_db)):
    """
    Alternative signup endpoint that returns token immediately
    """
    # Check if user already exists
    existing = crud.get_user_by_username(db, credentials.username)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    # Create user
    user = crud.create_user(
        db,
        username=credentials.username,
        email=None,
        password=credentials.password
    )
    
    # Return token immediately
    return TokenResponse(
        access_token=f"user_{user.id}_{user.username}",
        token_type="bearer"
    )