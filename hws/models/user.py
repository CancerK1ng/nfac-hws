from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id: int
    username: str
    email: str
    hashed_password: str
    photo_url: Optional[str] = None