from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app import crud, schemas

router = APIRouter(prefix="/borrow", tags=["borrow"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def borrow_book(
    borrow_in: schemas.borrow_record.BorrowCreate,
    db: Session = Depends(get_db),
):
    # Verify book availability inside CRUD layer
    record = crud.borrow.create_borrow_record(db, obj_in=borrow_in)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to create borrow record",
        )
    return record
