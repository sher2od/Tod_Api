from typing import List
from fastapi import APIRouter
from sqlalchemy import select

from app.database import LocalSession
from app.models.user import User
from app.schemas.users import UserCreate, UserOut

router = APIRouter(
    prefix="/users",
    tags=["User Endpoints"]
)


@router.post("/", response_model=UserOut)
async def create_user(user: UserCreate):
    async with LocalSession() as session:
        new_user = User(**user.model_dump())
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user


@router.get("/", response_model=List[UserOut])
async def get_users():
    async with LocalSession() as session:
        result = await session.execute(select(User))
        return result.scalars().all()
