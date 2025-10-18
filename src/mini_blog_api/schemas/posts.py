from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from typing import List
from .comments import CommentOut


class PostCreate(BaseModel):
    """Datos requeridos para crear una publicación."""
    title: str = Field(..., min_length=1, max_length=200)
    content: str
    author_id: int


class PostOut(BaseModel):
    """Datos devueltos al listar o consultar publicaciones."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    author_id: int
    created_at: datetime
    comments: List[CommentOut] = Field(default_factory=list)
