from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field

# -------- Users --------
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr
    created_at: datetime


# -------- Comments --------
class CommentCreate(BaseModel):
    text: str
    author_id: int


class CommentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    text: str
    author_id: int
    created_at: datetime


# -------- Posts --------
class PostCreate(BaseModel):
    title: str
    content: str
    author_id: int


class PostOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    author_id: int
    created_at: datetime
    comments: list[CommentOut] = Field(default_factory=list)
