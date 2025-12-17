from typing import List, Optional
from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.database import LocalSession
from app.models.task import Task
from app.models.user import User
from app.schemas.tasks import TaskCreate, TaskOut, TaskUpdate

router = APIRouter(
    prefix="/tasks",
    tags=["Task Endpoints"]
)


@router.post("/", response_model=TaskOut)
async def create_task(task: TaskCreate):
    async with LocalSession() as session:
        new_task = Task(**task.model_dump())
        session.add(new_task)
        await session.commit()
        await session.refresh(new_task)
        return new_task


@router.get("/", response_model=List[TaskOut])
async def get_tasks(
    status: Optional[str] = None,
    project_id: Optional[int] = None
):
    async with LocalSession() as session:
        query = select(Task)

        if status:
            query = query.where(Task.status == status)
        if project_id:
            query = query.where(Task.project_id == project_id)

        result = await session.execute(query)
        return result.scalars().all()


@router.get("/{task_id}", response_model=TaskOut)
async def get_task(task_id: int):
    async with LocalSession() as session:
        task = await session.get(Task, task_id)
        if not task:
            raise HTTPException(404, "Task not found")
        return task


@router.put("/{task_id}", response_model=TaskOut)
async def update_task(task_id: int, data: TaskUpdate):
    async with LocalSession() as session:
        task = await session.get(Task, task_id)
        if not task:
            raise HTTPException(404, "Task not found")

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(task, key, value)

        await session.commit()
        await session.refresh(task)
        return task


@router.delete("/{task_id}")
async def delete_task(task_id: int):
    async with LocalSession() as session:
        task = await session.get(Task, task_id)
        if not task:
            raise HTTPException(404, "Task not found")

        await session.delete(task)
        await session.commit()
        return {"detail": "Task deleted"}


@router.post("/{task_id}/assign")
async def assign_users(task_id: int, user_ids: List[int]):
    async with LocalSession() as session:
        task = await session.get(Task, task_id)
        if not task:
            raise HTTPException(404, "Task not found")

        users = await session.execute(
            select(User).where(User.id.in_(user_ids))
        )
        task.users.extend(users.scalars().all())

        await session.commit()
        return {"detail": "Users assigned"}


@router.post("/{task_id}/unassign")
async def unassign_users(task_id: int, user_ids: List[int]):
    async with LocalSession() as session:
        task = await session.get(Task, task_id)
        if not task:
            raise HTTPException(404, "Task not found")

        task.users = [u for u in task.users if u.id not in user_ids]
        await session.commit()
        return {"detail": "Users unassigned"}
