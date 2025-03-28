from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from api.db import Base


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True)
    title = Column(String(1024))

    done = relationship("Done", back_populates="task", cascade="delete")


class Done(Base):
    __tablename__ = "done"

    id = Column(Integer, ForeignKey("task.id"), primary_key=True)

    task = relationship("Task", back_populates="done")


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
