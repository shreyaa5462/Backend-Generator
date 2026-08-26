from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.book import Book as BookModel
from app.schemas.book import BookCreate, BookUpdate, Book as BookSchema


def get_book(db: Session, book_id: int) -> BookSchema:
    stmt = select(BookModel).where(BookModel.id == book_id)
    result = db.execute(stmt).scalar_one_or_none()
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return BookSchema.from_orm(result)


def get_books(db: Session, skip: int = 0, limit: int = 100) -> list[BookSchema]:
    stmt = select(BookModel).offset(skip).limit(limit)
    results = db.execute(stmt).scalars().all()
    return [BookSchema.from_orm(book) for book in results]


def create_book(db: Session, book_in: BookCreate) -> BookSchema:
    db_book = BookModel(**book_in.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return BookSchema.from_orm(db_book)


def update_book(db: Session, book_id: int, book_in: BookUpdate) -> BookSchema:
    db_book = db.get(BookModel, book_id)
    if db_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    for field, value in book_in.dict(exclude_unset=True).items():
        setattr(db_book, field, value)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return BookSchema.from_orm(db_book)


def delete_book(db: Session, book_id: int) -> None:
    db_book = db.get(BookModel, book_id)
    if db_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    db.delete(db_book)
    db.commit()
