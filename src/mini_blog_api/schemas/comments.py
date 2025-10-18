from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class CommentCreate(BaseModel):
    """Datos requeridos para crear un comentario."""
    text: str = Field(..., min_length=1, max_length=2000)
    author_id: int


class CommentOut(BaseModel):
    """Datos devueltos al listar o crear comentarios."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    text: str
    author_id: int
    created_at: datetime
