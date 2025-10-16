from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload

from mini_blog_api.core.database import get_session
from mini_blog_api.models import Post, User
from mini_blog_api.schemas import PostCreate, PostOut

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", response_model=PostOut, status_code=status.HTTP_201_CREATED)
async def create_post(payload: PostCreate, session: AsyncSession = Depends(get_session)):
    # validar autor
    author = await session.get(User, payload.author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Autor no existe")

    post = Post(
        title=payload.title,
        content=payload.content,
        author_id=payload.author_id,
    )
    session.add(post)
    await session.commit()

    # recargar con comentarios en eager (evita lazy-load en serialización)
    result = await session.execute(
        select(Post)
        .options(selectinload(Post.comments))
        .where(Post.id == post.id)
    )
    post = result.scalar_one()
    return post


@router.get("/", response_model=list[PostOut])
async def list_posts(
    limit: int = Query(10, ge=1, le=100),
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(Post)
        .options(selectinload(Post.comments))
        .order_by(desc(Post.created_at))
        .limit(limit)
    )
    return result.scalars().all()


@router.get("/{post_id}", response_model=PostOut)
async def get_post(post_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(Post)
        .options(selectinload(Post.comments))
        .where(Post.id == post_id)
    )
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    return post
