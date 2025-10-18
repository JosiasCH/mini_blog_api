from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from mini_blog_api.models import Post, Comment, User
from mini_blog_api.schemas import CommentCreate

async def add_comment(post_id: int, payload: CommentCreate, session: AsyncSession) -> Comment:
    post = await session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post no encontrado")

    author = await session.get(User, payload.author_id)
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Autor no existe")

    comment = Comment(text=payload.text, author_id=payload.author_id, post_id=post_id)
    session.add(comment)
    await session.commit()
    await session.refresh(comment)
    return comment

async def list_comments(post_id: int, session: AsyncSession) -> list[Comment]:
    post = await session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post no encontrado")

    result = await session.execute(
        select(Comment).where(Comment.post_id == post_id).order_by(Comment.created_at.asc())
    )
    return result.scalars().all()
