from datetime import datetime
import enum
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base

class BorrowStatus(enum.Enum):
    borrowed = "borrowed"
    returned = "returned"

class BorrowRecord(Base):
    __tablename__ = "borrow_records"

    id: int = Column(Integer, primary_key=True, index=True)
    user_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id: int = Column(Integer, ForeignKey("books.id"), nullable=False)
    borrow_date: datetime = Column(DateTime, default=datetime.utcnow, nullable=False)
    return_date: datetime = Column(DateTime, nullable=True)
    status: BorrowStatus = Column(Enum(BorrowStatus), default=BorrowStatus.borrowed, nullable=False)

    user = relationship("User", back_populates="borrow_records")
    book = relationship("Book", back_populates="borrow_records")
