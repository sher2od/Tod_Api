from sqlalchemy import (
    Column, Integer, String, Text, DateTime,
    ForeignKey, Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.database import Base
from app.models.task_user import task_users   


class TaskStatus(enum.Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)

    project_id = Column(
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False
    )

    title = Column(String(255), nullable=False)
    description = Column(Text)

    status = Column(Enum(TaskStatus), default=TaskStatus.todo)
    priority = Column(Integer)
    due_date = Column(DateTime)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    project = relationship("Project", back_populates="tasks")

    users = relationship(
        "User",
        secondary=task_users,  
        back_populates="tasks"
    )
