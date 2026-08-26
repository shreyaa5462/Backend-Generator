from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class BookBase(BaseModel):
    title: str
    author: str
    category: str
    available: bool = True

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None
    available: Optional[bool] = None

class BookResponse(BookBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
