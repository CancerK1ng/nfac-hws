from pydantic import BaseModel
from datetime import datetime

class CommentCreate(BaseModel):
    text: str
    category: str

class CommentResponse(BaseModel):
    id: int
    text: str
    category: str
    timestamp: datetime