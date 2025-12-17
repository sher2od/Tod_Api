from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.task_user import task_users


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)

    tasks = relationship(
        "Task",
        secondary=task_users,
        back_populates="users"
    )
