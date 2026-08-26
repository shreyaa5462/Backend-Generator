from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User as UserModel
from app.schemas.user import UserCreate, UserUpdate, User as UserSchema


def get_user(db: Session, user_id: int) -> UserSchema:
    stmt = select(UserModel).where(UserModel.id == user_id)
    result = db.execute(stmt).scalar_one_or_none()
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserSchema.from_orm(result)


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[UserSchema]:
    stmt = select(UserModel).offset(skip).limit(limit)
    results = db.execute(stmt).scalars().all()
    return [UserSchema.from_orm(user) for user in results]


def create_user(db: Session, user_in: UserCreate) -> UserSchema:
    db_user = UserModel(**user_in.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserSchema.from_orm(db_user)


def update_user(db: Session, user_id: int, user_in: UserUpdate) -> UserSchema:
    db_user = db.get(UserModel, user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    for field, value in user_in.dict(exclude_unset=True).items():
        setattr(db_user, field, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserSchema.from_orm(db_user)


def delete_user(db: Session, user_id: int) -> None:
    db_user = db.get(UserModel, user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(db_user)
    db.commit()
