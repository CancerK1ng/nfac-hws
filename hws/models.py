from sqlalchemy import Column, Integer, String, DateTime
from database import Base
import datetime

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(500), nullable=False)
    category = Column(String(20), nullable=False)  # "positive" или "negative"
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)