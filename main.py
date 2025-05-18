from fastapi import FastAPI
from app.routers import users, shanyraks, comments

app = FastAPI()

app.include_router(users.router)
app.include_router(shanyraks.router)
app.include_router(comments.router)
