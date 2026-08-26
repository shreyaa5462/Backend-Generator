from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional

class BorrowRecordBase(BaseModel):
    user_id: int
    book_id: int
    borrow_date: datetime = Field(default_factory=datetime.utcnow)
    return_date: Optional[datetime] = None
    status: str = "borrowed"

class BorrowRecordCreate(BorrowRecordBase):
    pass

class BorrowRecordUpdate(BaseModel):
    return_date: Optional[datetime] = None
    status: Optional[str] = None

class BorrowRecordResponse(BorrowRecordBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
