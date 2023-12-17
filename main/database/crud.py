from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from . import models

def create_user(db: Session, user: models.User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user.id

def get_user(db: Session, user_id):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_tasks(db: Session, user_id):
    print(db.query(models.Task).all())
    tasks = db.query(models.Task).filter(models.Task.user_id == user_id).all()
    print(tasks)
    return tasks

def create_task(db: Session, task: models.Task):
    db.add(task)
    db.commit()
    db.refresh(task)
    print(db.query(models.Task).all())
    return task

def get_task(db: Session, task_id: int, user_id):
    return db.query(models.Task).filter(models.Task.id == task_id).filter(models.Task.user_id == user_id).first()

def delete_task(db: Session, task_id: int, user_id):
    task = get_task(db, task_id, user_id)
    if task is None:
        return False
    db.delete(task)
    db.commit()
    return True

def update_task(db: Session, task_id: int, updated_task: models.Task, user_id):
    task = get_task(db, task_id, user_id)
    task.title = updated_task.title
    task.theme = updated_task.theme
    task.text = updated_task.text
    db.commit()

def switch_task_status(db: Session, task_id, new_status):
    task = db.query(models.Task).filter_by(id=task_id).first()
    if task:
        task.status = new_status
        db.commit()
        return True
    else:
        return False

def get_tasks_by_status(db: Session, status):
    tasks = db.query(models.Task).filter_by(status=status).all()
    return tasks