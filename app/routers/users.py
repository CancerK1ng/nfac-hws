from fastapi import APIRouter

router = APIRouter(prefix="/auth/users", tags=["users"])

@router.post("/")
def signup():
    return {"message": "User registered"}

@router.post("/login")
def login():
    return {"access_token": "<jwt_token>"}

@router.patch("/me")
def update_user():
    return {"message": "User updated"}

@router.get("/me")
def get_user():
    return {
        "id": 1,
        "username": "test@gmail.com",
        "phone": "+7 700 698 5025",
        "name": "Далида Е.",
        "city": "Алматы"
    }
