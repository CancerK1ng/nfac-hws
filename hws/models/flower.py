from pydantic import BaseModel

class Flower(BaseModel):
    id: int
    name: str
    cost: float
    count: int