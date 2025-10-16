from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from mini_blog_api.core.database import get_session
from mini_blog_api.models import Comment, Post, User
from mini_blog_api.schemas import CommentCreate, CommentOut

router = APIRouter(prefix="/posts/{post_id}/comments", tags=["comments"])

@router.post("/", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
async def create_comment(post_id: int, payload: CommentCreate, db: AsyncSession = Depends(get_session)):
    if not await db.get(Post, post_id):
        raise HTTPException(status_code=404, detail="post not found")
    if not await db.get(User, payload.author_id):
        raise HTTPException(status_code=404, detail="author not found")
    comment = Comment(text=payload.text, post_id=post_id, author_id=payload.author_id)
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment
