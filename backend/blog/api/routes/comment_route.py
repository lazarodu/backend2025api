from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from blog.usecases.comment.add_comment import AddCommentUseCase
from blog.usecases.comment.delete_comment import DeleteCommentUseCase
from blog.usecases.comment.get_comments_by_post import GetCommentsByPostUseCase
from blog.usecases.comment.get_comments_by_user import GetCommentsByUserUseCase
from blog.domain.entities.comment import Comment
import uuid
from blog.api.schemas.comment_schema import AddCommentInput, CommentOutput
from blog.domain.repositories.comment_repository import CommentRepository
from sqlalchemy.ext.asyncio import AsyncSession
from blog.api.deps import get_db_session, get_user_repository, get_current_user
from blog.infra.repositories.sqlalchemy.sqlalchemy_comment_repository import (
    SQLAlchemyCommentRepository,
)


router = APIRouter()


@router.get("/post/{post_id}", response_model=CommentOutput)
def get_comments_by_post(post_id: str, comment_repo: CommentRepository = Depends()):
    usecase = GetCommentsByPostUseCase(comment_repo)
    comments = usecase.execute(post_id)
    return comments


@router.get("/user/{user_id}", response_model=CommentOutput)
def get_comments_by_user(
    user_id: str, comment_repo: CommentRepository = Depends(get_user_repository)
):
    usecase = GetCommentsByUserUseCase(comment_repo)
    comments = usecase.execute(user_id)
    return comments


@router.post("/", response_model=CommentOutput)
def add_comment(data: AddCommentInput, db: AsyncSession = Depends(get_db_session)):
    comment_repo = SQLAlchemyCommentRepository(db)
    comment = Comment(
        id=str(uuid.uuid4()),
        post_id=data.post_id,
        user_id=data.user_id,
        comment=data.comment,
        date=data.date,
    )
    usecase = AddCommentUseCase(comment_repo)
    added_comment = usecase.execute(comment)
    return added_comment


@router.delete("/{comment_id}")
def delete_comment(
    comment_id: str, comment_repo: CommentRepository = Depends(get_user_repository)
):
    usecase = DeleteCommentUseCase(comment_repo)
    success = usecase.execute(comment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Comment not found")
    return {"message": "Comment deleted successfully"}
