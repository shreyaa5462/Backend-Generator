from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app import crud, schemas

router = APIRouter(prefix="/return", tags=["return"])

@router.post("/", status_code=status.HTTP_200_OK)
def return_book(
    return_in: schemas.borrow_record.ReturnCreate,
    db: Session = Depends(get_db),
):
    updated = crud.borrow.return_book(db, obj_in=return_in)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to process return",
        )
    return updated
