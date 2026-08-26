from fastapi import APIRouter, Depends, Query
from typing import List
from sqlalchemy.orm import Session

from app.database.session import get_db
from app import crud, schemas

router = APIRouter(prefix="/search", tags=["search"])

@router.get("/books", response_model=List[schemas.book.BookRead])
def search_books(
    query: str = Query(..., description="Search term for title or author"),
    db: Session = Depends(get_db),
):
    # Delegates to a CRUD search helper; implementation resides in crud.book
    return crud.book.search_books(db, term=query)
