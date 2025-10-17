from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.hash import bcrypt

from mini_blog_api.core.database import get_session
from mini_blog_api.models import User
from mini_blog_api.schemas import UserCreate, UserOut

router = APIRouter(prefix="/users", tags=["users"])

# ✅ Con barra final: /users/
@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate, session: AsyncSession = Depends(get_session)):
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

@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return user
