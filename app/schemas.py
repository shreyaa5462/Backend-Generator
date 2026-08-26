from typing import Any

from pydantic import BaseModel


class UploadResponse(BaseModel):
    message: str
    filename: str
    content: Any