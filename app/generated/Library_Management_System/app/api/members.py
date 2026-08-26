from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from app.database.session import get_db
from app import crud, schemas

router = APIRouter(prefix="/members", tags=["members"])

@router.get("/", response_model=List[schemas.user.UserRead])
def list_members(db: Session = Depends(get_db)):
    return crud.user.get_users(db)

@router.post("/", response_model=schemas.user.UserRead, status_code=status.HTTP_201_CREATED)
def create_member(
    user_in: schemas.user.UserCreate,
    db: Session = Depends(get_db),
):
    existing = crud.user.get_user_by_email(db, email=user_in.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    return crud.user.create_user(db, obj_in=user_in)
