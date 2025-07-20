# app/routers/boards.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/boards/")
def create_board(name: str, db: Session = Depends(get_db)):
    existing = db.query(models.Board).filter_by(name=name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Board already exists")
    board = models.Board(name=name)
    db.add(board)
    db.commit()
    db.refresh(board)
    return {"id": board.id, "name": board.name}

@router.get("/boards/")
def list_boards(db: Session = Depends(get_db)):
    return db.query(models.Board).all()
