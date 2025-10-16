from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from mini_blog_api.core.database import get_session
from mini_blog_api.models import Post, User
from mini_blog_api.schemas import PostCreate, PostOut, PostWithComments

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/", response_model=PostOut, status_code=status.HTTP_201_CREATED)
async def create_post(payload: PostCreate, db: AsyncSession = Depends(get_session)):
    if not await db.get(User, payload.author_id):
        raise HTTPException(status_code=404, detail="author not found")
    post = Post(title=payload.title, content=payload.content, author_id=payload.author_id)
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post

@router.get("/", response_model=list[PostOut])
async def list_posts(limit: int = Query(10, ge=1, le=100), db: AsyncSession = Depends(get_session)):
    stmt = select(Post).order_by(Post.created_at.desc()).limit(limit)
    return (await db.execute(stmt)).scalars().all()

@router.get("/{post_id}", response_model=PostWithComments)
async def get_post(post_id: int, db: AsyncSession = Depends(get_session)):
    stmt = select(Post).options(selectinload(Post.comments)).where(Post.id == post_id)
    post = (await db.execute(stmt)).scalars().first()
    if not post:
        raise HTTPException(status_code=404, detail="post not found")
    return post
