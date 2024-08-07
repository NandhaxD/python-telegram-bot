
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Text, Integer, select
from typing import List
import asyncio
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

from nandha.sql import engine, Base

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    bio: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"<User {self.username}>"

    async_sessionmaker_ = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    @classmethod
    async def add_user(cls, user_data: dict):
        async with cls.async_sessionmaker_() as session:
            async with session.begin():
                user = cls(**user_data)
                session.add(user)
                await session.commit()

    @classmethod
    async def get_user(cls, user_id: int):
        async with cls.async_sessionmaker_() as session:
            statement = select(cls).where(cls.id == user_id)
            result = await session.execute(statement)
            user = result.scalars().one()
            return user

    @classmethod
    async def update_user(cls, user_id: int, user_data: dict):
        async with cls.async_sessionmaker_() as session:
            statement = select(cls).where(cls.id == user_id)
            result = await session.execute(statement)
            user = result.scalars().one()
            user.username = user_data['username']
            user.email = user_data['email']
            user.bio = user_data['bio']
            await session.commit()

    @classmethod
    async def delete_user(cls, user_id: int):
        async with cls.async_sessionmaker_() as session:
            statement = select(cls).where(cls.id == user_id)
            result = await session.execute(statement)
            user = result.scalars().one()
            await session.delete(user)
            await session.commit()

