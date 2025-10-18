from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from mini_blog_api.core.database import get_session
from mini_blog_api.schemas import PostCreate, PostOut
from mini_blog_api.services import create_post, list_posts, get_post

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/", response_model=PostOut, status_code=status.HTTP_201_CREATED)
async def create_post_ep(payload: PostCreate, session: AsyncSession = Depends(get_session)):
    return await create_post(payload, session)

@router.get("/", response_model=list[PostOut])
async def list_posts_ep(
    limit: int = Query(10, ge=1, le=100),
    session: AsyncSession = Depends(get_session),
):
    return await list_posts(limit, session)

@router.get("/{post_id}", response_model=PostOut)
async def get_post_ep(post_id: int, session: AsyncSession = Depends(get_session)):
    return await get_post(post_id, session)
