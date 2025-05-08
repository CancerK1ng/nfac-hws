from typing import Optional, List
from models.user import User

class UsersRepository:
    def __init__(self):
        self.users: List[User] = []
        self.current_id = 1

    def create(self, username: str, email: str, hashed_password: str, photo_url: Optional[str] = None) -> User:
        user = User(
            id=self.current_id,
            username=username,
            email=email,
            hashed_password=hashed_password,
            photo_url=photo_url
        )
        self.users.append(user)
        self.current_id += 1
        return user

    def get_by_email(self, email: str) -> Optional[User]:
        for user in self.users:
            if user.email == email:
                return user
        return None

    def get_by_id(self, user_id: int) -> Optional[User]:
        for user in self.users:
            if user.id == user_id:
                return user
        return None