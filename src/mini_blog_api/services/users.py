from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from fastapi import HTTPException, status
from passlib.hash import bcrypt

from mini_blog_api.models import User
from mini_blog_api.schemas import UserCreate

async def create_user(payload: UserCreate, session: AsyncSession) -> User:
    user = User(
        username=payload.username,
        email=payload.email,
        password_hash=bcrypt.hash(payload.password[:72]),
    )
    session.add(user)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Usuario ya existe")
    await session.refresh(user)
    return user

async def get_user(user_id: int, session: AsyncSession) -> User:
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return user
