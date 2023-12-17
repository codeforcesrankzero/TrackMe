from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Task, User
from database.database import get_db
import database.crud as crud
from openai import OpenAI


app = FastAPI()
from typing import Optional

class TaskModel(BaseModel):
    title: str
    text: Optional[str]
    theme: Optional[str]

class UserModel(BaseModel):
    username: str
    user_id: int

class PrettifyModel(BaseModel):
    text: str

@app.post("/create_user")
async def create_task(user: UserModel, db: Session = Depends(get_db)):
    db_user = User(id=user.user_id, username=user.username)
    return {"id": crud.create_user(db, db_user)}


@app.get("/get_user")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user =  crud.get_user(db, user_id)
    print(user)
    if user is None:
        return None
    return user

@app.post("/create_task")
async def create_task(task: TaskModel, user_id: int, db: Session = Depends(get_db)):
    db_task = Task(title=task.title, theme=task.theme, text=task.text, user_id=user_id)
    crud.create_task(db, db_task)
    print(db_task.user_id)
    return {"task": "Task created!"}

@app.delete("/delete_task")
async def delete_task(task_id: int, user_id: int, db: Session = Depends(get_db)):
   return crud.delete_task(db, task_id, user_id)


@app.put("/switch_status")
async def switch_status(new_status: str, task_id: int,  db: Session = Depends(get_db)):
    print("STAT", new_status)
    return crud.switch_task_status(db, task_id, new_status)

@app.get("/get_by_status")
async def switch_status(status: str, db: Session = Depends(get_db)):
    return crud.get_tasks_by_status(db, status)

@app.get("/get_tasks")
async def get_tasks(user_id: int, db: Session = Depends(get_db)):
    return crud.get_tasks(db, user_id)


@app.get("/get_task")
async def get_task(task_id: int, user_id: int, db: Session = Depends(get_db)):
    return crud.get_task(db, task_id, user_id)

@app.put("/modify_task")
async def modify_task(task_id: int, user_id: int, new_task: TaskModel, db: Session = Depends(get_db)):
    new_db_task = Task(title=new_task.title, theme=new_task.theme, text=new_task.text)
    crud.update_task(db, task_id, new_db_task, user_id)

@app.get("/get_better")
async def get_better(text: PrettifyModel, db: Session = Depends(get_db)):
    client = OpenAI(
        api_key="",
        base_url="https://api.proxyapi.ru/openai/v1",
    )

    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"Please make this text: {text} prettier, more work-ethical and replace it by a task for task system out of this text. Do not overiamgine it, just make it better in given terms. Your answer should be in the language of original text, which is Russian"}]
    )
    print(chat_completion)
    return {"task": chat_completion.choices[0].message.content}