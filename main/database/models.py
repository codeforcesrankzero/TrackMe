
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)
    text = Column(String, nullable=True)
    theme = Column(String, nullable=True)
    due_date = Column(DateTime, nullable=True)
    add_date = Column(DateTime, nullable=True, default=datetime.utcnow)