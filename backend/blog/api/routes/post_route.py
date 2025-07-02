from fastapi import APIRouter, HTTPException, Depends
from blog.usecases.post.create_post import CreatePostUseCase
from blog.usecases.post.delete_post import DeletePostUseCase
from blog.usecases.post.get_all_posts import GetAllPostsUseCase
from blog.usecases.post.get_post_by_id import GetPostByIdUseCase
from blog.usecases.post.update_post import UpdatePostUseCase
from blog.domain.entities.post import Post
from blog.domain.entities.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from blog.api.deps import get_user_repository, get_current_user, get_db_session

from blog.domain.repositories.post_repository import PostRepository

from blog.api.schemas.post_schema import PostCreateInput

import uuid
from blog.api.schemas.post_schema import PostOutput, PostCreateInput, PostUpdateInput
from blog.infra.repositories.sqlalchemy.sqlalchemy_post_repository import (
    SQLAlchemyPostRepository,
)


router = APIRouter()


@router.get("/", response_model=PostOutput)
def get_all_posts(
    user: User = Depends(get_current_user),
    post_repo: PostRepository = Depends(get_user_repository),
):
    usecase = GetAllPostsUseCase(post_repo)
    posts = usecase.execute()
    return posts


@router.get("/{post_id}", response_model=PostOutput)
def get_post_by_id(
    post_id: str, post_repo: PostRepository = Depends(get_user_repository)
):
    usecase = GetPostByIdUseCase(post_repo)
    post = usecase.execute(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.post("/", response_model=PostOutput)
def create_post(data: PostCreateInput, db: AsyncSession = Depends(get_db_session)):
    post_repo = SQLAlchemyPostRepository(db)
    usecase = CreatePostUseCase(post_repo)
    post = Post(
        id=str(uuid.uuid4()),
        title=data.title,
        description=data.description,
        content=data.content,
        user_id=data.user_id,
        date=data.date,
    )
    created_post = usecase.execute(post)
    return created_post


@router.put("/{post_id}", response_model=PostOutput)
def update_post(
    post_id: str,
    data: PostUpdateInput,
    post_repo: PostRepository = Depends(get_user_repository),
):
    usecase_get = GetPostByIdUseCase(post_repo)
    existing_post = usecase_get.execute(post_id)
    if not existing_post:
        raise HTTPException(status_code=404, detail="Post not found")

    updated_post = Post(
        id=post_id,
        title=data.title,
        description=data.description,
        content=data.content,
        user_id=existing_post.user_id,
        date=existing_post.date,
    )
    usecase_update = UpdatePostUseCase(post_repo)
    result = usecase_update.execute(updated_post)
    return result


@router.delete("/{post_id}")
def delete_post(post_id: str, post_repo: PostRepository = Depends(get_user_repository)):
    usecase = DeletePostUseCase(post_repo)
    success = usecase.execute(post_id)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post deleted successfully"}
