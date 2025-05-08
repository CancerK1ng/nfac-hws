from sqlalchemy.orm import Session
import models

def create_comment(db: Session, comment: schemas.CommentCreate):
    db_comment = models.Comment(**comment.dict())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comments(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Comment).offset(skip).limit(limit).all()