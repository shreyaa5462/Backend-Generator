from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from app import models, schemas


def get_borrow_record(db: Session, record_id: int) -> models.BorrowRecord:
    stmt = select(models.BorrowRecord).where(models.BorrowRecord.id == record_id)
    result = db.execute(stmt).scalar_one_or_none()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Borrow record not found")
    return result


def get_borrow_records(db: Session, skip: int = 0, limit: int = 100) -> List[models.BorrowRecord]:
    stmt = select(models.BorrowRecord).offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()


def create_borrow_record(db: Session, record_in: schemas.BorrowRecordCreate) -> models.BorrowRecord:
    # Ensure related user and book exist
    user = db.get(models.User, record_in.user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    book = db.get(models.Book, record_in.book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    if not book.available:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book is not available")

    db_record = models.BorrowRecord(**record_in.dict())
    db.add(db_record)
    # Mark book as unavailable
    book.available = False
    db.add(book)
    db.commit()
    db.refresh(db_record)
    return db_record


def update_borrow_record(db: Session, record_id: int, record_in: schemas.BorrowRecordUpdate) -> models.BorrowRecord:
    db_record = get_borrow_record(db, record_id)
    update_data = record_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_record, field, value)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def delete_borrow_record(db: Session, record_id: int) -> None:
    db_record = get_borrow_record(db, record_id)
    # If the book was borrowed, make it available again
    if db_record.book_id:
        book = db.get(models.Book, db_record.book_id)
        if book:
            book.available = True
            db.add(book)
    db.delete(db_record)
    db.commit()
