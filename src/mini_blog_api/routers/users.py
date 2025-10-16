from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from passlib.hash import bcrypt
from mini_blog_api.core.database import get_session
from mini_blog_api.models import User
from mini_blog_api.schemas import UserCreate, UserOut

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate, db: AsyncSession = Depends(get_session)):
    exists = await db.scalar(select(User.id).where(or_(User.username == payload.username, User.email == payload.email)))
    if exists:
        raise HTTPException(status_code=409, detail="username or email already exists")
    user = User(username=payload.username, email=payload.email, password_hash=bcrypt.hash(payload.password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user
