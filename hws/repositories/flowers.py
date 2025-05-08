from typing import List
from models.flower import Flower

class FlowersRepository:
    def __init__(self):
        self.flowers: List[Flower] = []
        self.current_id = 1

    def create(self, name: str, cost: float, count: int) -> Flower:
        flower = Flower(
            id=self.current_id,
            name=name,
            cost=cost,
            count=count
        )
        self.flowers.append(flower)
        self.current_id += 1
        return flower

    def get_all(self) -> List[Flower]:
        return self.flowers

    def get_by_ids(self, ids: List[int]) -> List[Flower]:
        return [flower for flower in self.flowers if flower.id in ids]