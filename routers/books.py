# routers/books.py
from typing import List
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import crud
import schemas
import google_books

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/search")
def search_books(
    q: str = Query(..., min_length=1, description="Search query"), 
    max_results: int = Query(8, ge=1, le=40, description="Maximum results to return")
):
    """
    Search for books using Google Books API
    """
    try:
        return google_books.search_google_books(q, max_results=max_results)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching books: {str(e)}"
        )


@router.get("/", response_model=List[schemas.BookOut])
def list_books(db: Session = Depends(get_db)):
    """
    Get all books in the database
    """
    return crud.list_books(db)


@router.post("/", response_model=schemas.BookOut, status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    """
    Add a new book to the database
    """
    return crud.create_book(db, book)


@router.get("/{book_id}", response_model=schemas.BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """
    Get a specific book by ID
    """
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return book