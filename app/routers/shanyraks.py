from fastapi import APIRouter

router = APIRouter(prefix="/shanyraks", tags=["shanyraks"])

@router.post("/")
def create_shanyrak():
    return {"id": "1"}

@router.get("/{id}")
def get_shanyrak(id: int):
    return {
        "id": id,
        "type": "rent",
        "price": 150000,
        "address": "Астана, Алматы р-н, ул. Нажимеденова, 16 – Сарыколь",
        "area": 46.5,
        "rooms_count": 2,
        "description": "Описание квартиры...",
        "user_id": 1,
        "total_comments": 12
    }

@router.patch("/{id}")
def update_shanyrak(id: int):
    return {"message": "Shanyrak updated"}

@router.delete("/{id}")
def delete_shanyrak(id: int):
    return {"message": "Shanyrak deleted"}
