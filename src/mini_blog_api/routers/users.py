from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from mini_blog_api.core.database import get_session
from mini_blog_api.schemas import UserCreate, UserOut
from mini_blog_api.services import create_user, get_user as get_user_svc

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user_ep(payload: UserCreate, session: AsyncSession = Depends(get_session)):
    return await create_user(payload, session)

@router.get("/{user_id}", response_model=UserOut)
async def get_user_ep(user_id: int, session: AsyncSession = Depends(get_session)):
    return await get_user_svc(user_id, session)
