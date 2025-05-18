from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    phone = Column(String)
    name = Column(String)
    city = Column(String)

class Shanyrak(Base):
    __tablename__ = "shanyraks"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    price = Column(Integer)
    address = Column(String)
    area = Column(Float)
    rooms_count = Column(Integer)
    description = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))
    shanyrak_id = Column(Integer, ForeignKey("shanyraks.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
