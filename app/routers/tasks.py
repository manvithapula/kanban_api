# app/routers/tasks.py
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

@router.post("/columns/{column_str_id}/tasks", response_model=schemas.TaskOut)
def create_task(column_str_id: str, task: schemas.TaskCreate, db: Session = Depends(get_db)):
    column = db.query(models.Column).filter_by(column_str_id=column_str_id).first()
    if not column:
        raise HTTPException(status_code=404, detail="Column not found")

    existing_tasks = db.query(models.Task).filter_by(column_str_id=column_str_id).count()
    order = existing_tasks

    db_task = models.Task(**task.dict(), column_str_id=column_str_id, order_in_column=order)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/columns/{column_str_id}/tasks", response_model=list[schemas.TaskOut])
def get_tasks(column_str_id: str, db: Session = Depends(get_db)):
    column = db.query(models.Column).filter_by(column_str_id=column_str_id).first()
    if not column:
        raise HTTPException(status_code=404, detail="Column not found")

    return db.query(models.Task).filter_by(column_str_id=column_str_id).order_by(models.Task.order_in_column).all()

@router.put("/tasks/{task_str_id}/move", response_model=schemas.TaskOut)
def move_task(task_str_id: str, move: schemas.MoveTask, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter_by(task_str_id=task_str_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.column_str_id == move.target_column_str_id and task.order_in_column == move.new_order_in_column:
        return task  # No changes needed

    # Reorder tasks in source column
    source_tasks = db.query(models.Task).filter_by(column_str_id=task.column_str_id).order_by(models.Task.order_in_column).all()
    for t in source_tasks:
        if t.order_in_column > task.order_in_column:
            t.order_in_column -= 1

    # Reorder tasks in target column
    target_tasks = db.query(models.Task).filter_by(column_str_id=move.target_column_str_id).order_by(models.Task.order_in_column.desc()).all()
    for t in target_tasks:
        if t.order_in_column >= move.new_order_in_column:
            t.order_in_column += 1

    # Move task
    task.column_str_id = move.target_column_str_id
    task.order_in_column = move.new_order_in_column

    db.commit()
    db.refresh(task)
    return task
