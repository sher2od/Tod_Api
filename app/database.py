from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import config


DATABASE_URL = URL.create(
    drivername="postgresql+asyncpg",
    username=config.DB_USER,
    password=config.DB_PASS,
    host=config.DB_HOST,
    port=config.DB_PORT,
    database=config.DB_NAME,
)

engine = create_async_engine(DATABASE_URL, echo=True)

LocalSession = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()


async def initial_db():
    from app.models.project import Project
    from app.models.task import Task
    from app.models.user import User
    from app.models.task_user import task_users

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
