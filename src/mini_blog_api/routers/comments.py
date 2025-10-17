from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from mini_blog_api.core.database import get_session
from mini_blog_api.models import Post, Comment, User
from mini_blog_api.schemas import CommentCreate, CommentOut

router = APIRouter(prefix="/posts/{post_id}/comments", tags=["comments"])

# Acepta con y sin slash final para evitar 307
@router.post("", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
@router.post("/", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
async def add_comment(
    post_id: int,
    payload: CommentCreate,
    session: AsyncSession = Depends(get_session),
):
    post = await session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post no encontrado")

    author = await session.get(User, payload.author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Autor no existe")

    comment = Comment(
        text=payload.text,
        author_id=payload.author_id,
        post_id=post_id,
    )
    session.add(comment)
    await session.commit()
    await session.refresh(comment)
    return comment


# También para GET
@router.get("", response_model=list[CommentOut])
@router.get("/", response_model=list[CommentOut])
async def list_comments(post_id: int, session: AsyncSession = Depends(get_session)):
    post = await session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post no encontrado")

    result = await session.execute(
        select(Comment).where(Comment.post_id == post_id).order_by(Comment.created_at.asc())
    )
    return result.scalars().all()
