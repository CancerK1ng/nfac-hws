from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/comments/", response_model=schemas.CommentResponse)
def add_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    return crud.create_comment(db, comment)

@app.get("/comments/", response_model=list[schemas.CommentResponse])
def read_comments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_comments(db, skip=skip, limit=limit)