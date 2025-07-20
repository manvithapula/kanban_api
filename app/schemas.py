# app/schemas.py
from pydantic import BaseModel
from typing import Optional, List

class ColumnCreate(BaseModel):
    column_str_id: str
    name: str
    order_on_board: int

class ColumnOut(ColumnCreate):
    board_id: int

class TaskCreate(BaseModel):
    task_str_id: str
    title: str
    description: Optional[str] = None

class TaskOut(BaseModel):
    task_str_id: str
    title: str
    description: Optional[str]
    order_in_column: int
    column_str_id: str

    class Config:
        orm_mode = True

class MoveTask(BaseModel):
    target_column_str_id: str
    new_order_in_column: int
