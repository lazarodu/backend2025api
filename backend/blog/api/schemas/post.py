from pydantic import BaseModel, Field
from typing import Optional

class PostCreateInput(BaseModel):
    title: str = Field(..., min_length=3, max_length=100, description="Título do post")
    description: str = Field(..., min_length=10, max_length=300, description="Descrição do post")
    content: str = Field(..., min_length=20, description="Conteúdo do post")
    author: str = Field(..., description="Autor do post")

class PostUpdateInput(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None

class PostOutput(BaseModel):
    id: str = Field(..., description="ID do post")
    title: str = Field(..., min_length=3, max_length=100, description="Título do post")
    description: str = Field(..., min_length=10, max_length=300, description="Descrição do post")
    content: str = Field(..., min_length=20, description="Conteúdo do post")
    author: str = Field(..., description="Autor do post")
    date: str = Field(..., description="Data de criação do post")

    @classmethod
    def from_entity(cls, post):
        return cls(
            id=post.id,
            title=post.title,
            description=post.description,
            content=post.content,
            author=post.author,
            date=post.date
        )
