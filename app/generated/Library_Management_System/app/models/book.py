from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base

class Book(Base):
    __tablename__ = "books"

    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String, nullable=False)
    author: str = Column(String, nullable=False)
    category: str = Column(String, nullable=False)
    available: bool = Column(Boolean, default=True, nullable=False)

    borrow_records = relationship("BorrowRecord", back_populates="book", cascade="all, delete-orphan")
