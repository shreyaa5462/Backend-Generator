from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app import crud, schemas

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=schemas.user.UserRead)
def register_user(
    user_in: schemas.user.UserCreate,
    db: Session = Depends(get_db)
):
    existing = crud.user.get_user_by_email(db, email=user_in.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    return crud.user.create_user(db, obj_in=user_in)

@router.post("/login")
def login_user(
    credentials: schemas.user.UserLogin,
    db: Session = Depends(get_db)
):
    user = crud.user.authenticate_user(
        db,
        email=credentials.email,
        password=credentials.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    # JWT generation is omitted as per requirements
    return {"access_token": "dummy-token", "token_type": "bearer"}
