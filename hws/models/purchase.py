from pydantic import BaseModel

class Purchase(BaseModel):
    id: int
    user_id: int
    flower_id: int