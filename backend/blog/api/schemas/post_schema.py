from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any
from datetime import datetime
from blog.api.schemas.user_schema import UserOutput
from blog.domain.entities.post import Post
from blog.api.schemas.user_schema import user_to_output


class PostCreateInput(BaseModel):
    title: str = Field(..., min_length=3, max_length=200, description="Título do post")
    description: str = Field(
        ..., min_length=10, max_length=300, description="Descrição do post"
    )
    content: str = Field(..., min_length=20, description="Conteúdo do post")
    date: datetime = Field(..., description="Data de criação do post")


class PostUpdateInput(BaseModel):
    title: str = Field(..., min_length=3, max_length=200, description="Título do post")
    description: str = Field(
        ..., min_length=10, max_length=300, description="Descrição do post"
    )
    content: str = Field(..., min_length=20, description="Conteúdo do post")


class PostOutput(BaseModel):
    id: str = Field(..., description="ID do post")
    title: str = Field(..., min_length=3, max_length=100, description="Título do post")
    description: str = Field(
        ..., min_length=10, max_length=300, description="Descrição do post"
    )
    content: str = Field(..., min_length=20, description="Conteúdo do post")
    date: datetime = Field(..., description="Data de criação do post")
    user: UserOutput = Field(..., description="Dados do usuário que está postando")

    @classmethod
    def from_entity(cls, post):
        return cls(
            id=post.id,
            title=post.title,
            description=post.description,
            content=post.content,
            user_id=post.user_id,
            date=post.date,
            user=post.user,
        )


def post_to_output(post: Post) -> PostOutput:
    return PostOutput(
        id=post.id,
        title=post.title,
        content=post.content,
        description=post.description,
        date=post.date,
        user=user_to_output(post.user) if post.user else None,
    )


def posts_to_output(posts: list[Post]) -> list[PostOutput]:
    return [post_to_output(post) for post in posts]
