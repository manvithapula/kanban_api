# app/routers/columns.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/boards/{board_id}/columns", response_model=schemas.ColumnOut)
def create_column(board_id: int, column: schemas.ColumnCreate, db: Session = Depends(get_db)):
    # Check if board exists
    board = db.query(models.Board).filter_by(id=board_id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")

    # Check for duplicate column ID
    existing_column = db.query(models.Column).filter_by(column_str_id=column.column_str_id).first()
    if existing_column:
        raise HTTPException(status_code=400, detail="Column ID already exists")

    db_column = models.Column(**column.dict(), board_id=board_id)
    db.add(db_column)
    db.commit()
    db.refresh(db_column)
    return db_column
