from sqlalchemy.orm import Session
from . import models

def get_tasks(db: Session):
    return db.query(models.Task).all()

def create_task(db: Session, task: models.Task):
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def delete_task(db: Session, task_id: int):
    task = get_task(db, task_id)
    db.delete(task)
    db.commit()

def update_task(db: Session, task_id: int, updated_task: models.Task):
    task = get_task(db, task_id)
    task.title = updated_task.title
    task.theme = updated_task.theme
    task.text = updated_task.text
    db.commit()