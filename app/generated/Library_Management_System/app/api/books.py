from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional
from sqlalchemy.orm import Session

from app.database.session import get_db
from app import crud, schemas

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/", response_model=List[schemas.book.BookRead])
def list_books(
    title: Optional[str] = Query(None),
    author: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    available: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
):
    filters = {
        "title": title,
        "author": author,
        "category": category,
        "available": available,
    }
    # Remove None values
    filters = {k: v for k, v in filters.items() if v is not None}
    return crud.book.get_books(db, filters=filters)

@router.post("/", response_model=schemas.book.BookRead, status_code=status.HTTP_201_CREATED)
def create_book(
    book_in: schemas.book.BookCreate,
    db: Session = Depends(get_db),
):
    return crud.book.create_book(db, obj_in=book_in)

@router.put("/{book_id}", response_model=schemas.book.BookRead)
def update_book(
    book_id: int,
    book_in: schemas.book.BookUpdate,
    db: Session = Depends(get_db),
):
    existing = crud.book.get_book(db, book_id=book_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )
    return crud.book.update_book(db, db_obj=existing, obj_in=book_in)

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
):
    existing = crud.book.get_book(db, book_id=book_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )
    crud.book.delete_book(db, db_obj=existing)
    return None
