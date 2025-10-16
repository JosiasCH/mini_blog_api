from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import List

class UserCreate(BaseModel):
    username: str = Field(..., max_length=30)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    class Config:
        from_attributes = True

class PostCreate(BaseModel):
    title: str = Field(..., max_length=200)
    content: str
    author_id: int

class PostOut(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    author_id: int
    class Config:
        from_attributes = True

class CommentCreate(BaseModel):
    text: str
    author_id: int

class CommentOut(BaseModel):
    id: int
    text: str
    created_at: datetime
    author_id: int
    post_id: int
    class Config:
        from_attributes = True

class PostWithComments(PostOut):
    comments: List[CommentOut] = []
