
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    tasks = relationship("Task", back_populates="user")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)
    text = Column(String, nullable=True)
    theme = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    due_date = Column(DateTime, nullable=True)
    add_date = Column(DateTime, nullable=True, default=datetime.utcnow)
    user = relationship("User", back_populates="tasks")
    status = Column(Enum('open', 'in progress', 'closed'), default='open')
