from fastapi import FastAPI
from .database import Base, engine
from .routers import boards, columns, tasks

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(boards.router)
app.include_router(columns.router)
app.include_router(tasks.router)
