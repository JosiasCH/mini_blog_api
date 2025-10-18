from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status

from mini_blog_api.models import Post, User
from mini_blog_api.schemas import PostCreate

async def create_post(payload: PostCreate, session: AsyncSession) -> Post:
    author = await session.get(User, payload.author_id)
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Autor no existe")

    post = Post(title=payload.title, content=payload.content, author_id=payload.author_id)
    session.add(post)
    await session.commit()

    # recargar con relaciones para serialización correcta
    result = await session.execute(
        select(Post)
        .options(selectinload(Post.comments))
        .where(Post.id == post.id)
    )
    return result.scalar_one()

async def list_posts(limit: int, session: AsyncSession) -> list[Post]:
    result = await session.execute(
        select(Post)
        .options(selectinload(Post.comments))
        .order_by(desc(Post.created_at))
        .limit(limit)
    )
    return result.scalars().all()

async def get_post(post_id: int, session: AsyncSession) -> Post:
    result = await session.execute(
        select(Post)
        .options(selectinload(Post.comments))
        .where(Post.id == post_id)
    )
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post no encontrado")
    return post
