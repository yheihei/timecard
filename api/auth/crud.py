from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth import schemas
from api.auth.security import get_password_hash
from api.models import User


async def get_user(db: AsyncSession, user_id: str):
    result = await db.execute(
        select(User).filter(User.id == user_id)
    )
    return result.scalars().first()

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(
        select(User).filter(User.email == email)
    )
    return result.scalars().first()

async def get_user_by_username(db: AsyncSession, username: str | None):
    result = await db.execute(
        select(User).filter(User.username == username)
    )
    return result.scalars().first()

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    db_user = User(email=user.email, username=user.username, hashed_password=get_password_hash(user.password))
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user