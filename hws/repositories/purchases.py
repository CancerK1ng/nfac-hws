from typing import List
from models.purchase import Purchase

class PurchasesRepository:
    def __init__(self):
        self.purchases: List[Purchase] = []
        self.current_id = 1

    def create(self, user_id: int, flower_id: int) -> Purchase:
        purchase = Purchase(
            id=self.current_id,
            user_id=user_id,
            flower_id=flower_id
        )
        self.purchases.append(purchase)
        self.current_id += 1
        return purchase

    def get_by_user_id(self, user_id: int) -> List[Purchase]:
        return [purchase for purchase in self.purchases if purchase.user_id == user_id]