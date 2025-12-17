from fastapi import FastAPI

from app.database import engine, Base
from app.models.project import Project
from app.models.task import Task
from app.models.user import User

from app.routers.projects import router as projects_router
from app.routers.tasks import router as tasks_router
from app.routers.users import router as users_router


app = FastAPI(
    title="Todo Api"
)


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(projects_router)
app.include_router(tasks_router)
app.include_router(users_router)
