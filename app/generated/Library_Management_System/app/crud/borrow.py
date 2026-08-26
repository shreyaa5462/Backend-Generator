from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.models.borrow_record import BorrowRecord as BorrowModel
from app.schemas.borrow_record import BorrowRecordCreate, BorrowRecordUpdate, BorrowRecord as BorrowSchema
from app.models.book import Book as BookModel


def get_borrow_record(db: Session, record_id: int) -> BorrowSchema:
    stmt = select(BorrowModel).where(BorrowModel.id == record_id)
    result = db.execute(stmt).scalar_one_or_none()
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Borrow record not found")
    return BorrowSchema.from_orm(result)


def get_borrow_records(db: Session, skip: int = 0, limit: int = 100) -> list[BorrowSchema]:
    stmt = select(BorrowModel).offset(skip).limit(limit)
    results = db.execute(stmt).scalars().all()
    return [BorrowSchema.from_orm(rec) for rec in results]


def create_borrow_record(db: Session, borrow_in: BorrowRecordCreate) -> BorrowSchema:
    # Ensure the book exists and is available
    book = db.get(BookModel, borrow_in.book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    if not book.available:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book is not available for borrowing")

    db_record = BorrowModel(**borrow_in.dict())
    db.add(db_record)
    # Mark book as unavailable
    book.available = False
    db.add(book)
    db.commit()
    db.refresh(db_record)
    return BorrowSchema.from_orm(db_record)


def update_borrow_record(db: Session, record_id: int, borrow_in: BorrowRecordUpdate) -> BorrowSchema:
    db_record = db.get(BorrowModel, record_id)
    if db_record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Borrow record not found")
    for field, value in borrow_in.dict(exclude_unset=True).items():
        setattr(db_record, field, value)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return BorrowSchema.from_orm(db_record)


def delete_borrow_record(db: Session, record_id: int) -> None:
    db_record = db.get(BorrowModel, record_id)
    if db_record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Borrow record not found")
    # If the book was borrowed, make it available again
    if db_record.status == "borrowed":
        book = db.get(BookModel, db_record.book_id)
        if book:
            book.available = True
            db.add(book)
    db.delete(db_record)
    db.commit()
