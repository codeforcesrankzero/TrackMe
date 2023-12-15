from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Task
from database.database import get_db
import database.crud as crud

app = FastAPI()
from typing import Optional

class TaskModel(BaseModel):
    title: str
    text: Optional[str]
    theme: Optional[str]


@app.post("/create_task")
async def create_task(task: TaskModel, db: Session = Depends(get_db)):
    db_task = Task(title=task.title, theme=task.theme)
    created_task = crud.create_task(db, db_task)
    return {"task": "Task created!"}


@app.delete("/delete_task")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
   crud.delete_task(db, task_id)
   return {"task" : "Deleted!"}


@app.get("/get_tasks")
async def get_tasks(db: Session = Depends(get_db)):
    return crud.get_tasks(db)


@app.get("/get_task")
async def get_task(task_id: int, db: Session = Depends(get_db)):
    return crud.get_task(db, task_id)


@app.put("/modify_task")
async def modify_task(task_id: int, new_task: TaskModel, db: Session = Depends(get_db)):
    new_db_task = Task(title=new_task.title, theme=new_task.theme, text=new_task.text)
    crud.update_task(db, task_id, new_db_task)