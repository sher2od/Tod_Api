from typing import List

from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from sqlalchemy import select

from app.database import LocalSession
from app.models.project import Project
from app.schemas.projects import ProjectCreate, ProjectOut

router = APIRouter(
    prefix="/projects",
    tags=["Project Endpoints"]
)



@router.post("/", response_model=ProjectOut)
async def create_project(project: ProjectCreate):
    async with LocalSession() as session:
        new_project = Project(
            name=project.name,
            description=project.description
        )
        session.add(new_project)
        await session.commit()
        await session.refresh(new_project)
        return new_project



@router.get("/", response_model=List[ProjectOut])
async def get_projects():
    async with LocalSession() as session:
        result = await session.execute(select(Project))
        projects = result.scalars().all()
        return projects



@router.get("/{project_id}", response_model=ProjectOut)
async def get_project(project_id: int):
    async with LocalSession() as session:
        project = await session.get(Project, project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project
