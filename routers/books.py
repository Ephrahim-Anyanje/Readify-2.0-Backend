# routers/books.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
import crud, schemas, google_books

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/search")
def search(q: str = Query(..., min_length=1), max_results: int = 8):
    return google_books.search_google_books(q, max_results=max_results)

@router.get("/", response_model=list[schemas.BookOut])
def list_books(db: Session = Depends(get_db)):
    return crud.list_books(db)
