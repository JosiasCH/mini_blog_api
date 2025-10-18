from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from mini_blog_api.core.database import get_session
from mini_blog_api.schemas import CommentCreate, CommentOut
from mini_blog_api.services import add_comment, list_comments

router = APIRouter(prefix="/posts/{post_id}/comments", tags=["comments"])

@router.post("", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
@router.post("/", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
async def add_comment_ep(
    post_id: int,
    payload: CommentCreate,
    session: AsyncSession = Depends(get_session),
):
    return await add_comment(post_id, payload, session)

@router.get("", response_model=list[CommentOut])
@router.get("/", response_model=list[CommentOut])
async def list_comments_ep(post_id: int, session: AsyncSession = Depends(get_session)):
    return await list_comments(post_id, session)
