# app/models.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Board(Base):
    _tablename_ = "boards"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    columns = relationship("KanbanColumn", back_populates="board")

class KanbanColumn(Base):
    _tablename_ = "columns"
    column_str_id = Column(String(100), primary_key=True, index=True)
    name = Column(String(100))
    order_on_board = Column(Integer)
    board_id = Column(Integer, ForeignKey("boards.id"))
    board = relationship("Board", back_populates="columns")
    tasks = relationship("Task", back_populates="column")

class Task(Base):
    _tablename_ = "tasks"
    task_str_id = Column(String(100), primary_key=True, index=True)
    title = Column(String(100))
    description = Column(String(255), nullable=True)
    order_in_column = Column(Integer)
    column_str_id = Column(String(100), ForeignKey("columns.column_str_id"))
    column = relationship("KanbanColumn", back_populates="tasks")
