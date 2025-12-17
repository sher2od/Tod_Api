from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class TaskBase(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.todo
    priority: int = Field(..., ge=1, le=5)
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    project_id: int


class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    status: Optional[TaskStatus]
    priority: Optional[int] = Field(None, ge=1, le=5)
    due_date: Optional[datetime]


class TaskOut(TaskBase):
    id: int
    project_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
