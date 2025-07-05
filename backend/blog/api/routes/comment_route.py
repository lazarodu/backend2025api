from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from blog.usecases.comment.add_comment import AddCommentUseCase
from blog.usecases.comment.delete_comment import DeleteCommentUseCase
from blog.usecases.comment.get_comments_by_post import GetCommentsByPostUseCase
from blog.usecases.comment.get_comments_by_user import GetCommentsByUserUseCase
from blog.domain.entities.comment import Comment
from blog.domain.entities.user import User
import uuid
from blog.api.schemas.comment_schema import AddCommentInput, CommentOutput
from blog.domain.repositories.comment_repository import CommentRepository
from sqlalchemy.ext.asyncio import AsyncSession
from blog.api.deps import (
    get_db_session,
    get_user_repository,
    get_comment_repository,
    get_current_user,
)
from blog.infra.repositories.sqlalchemy.sqlalchemy_comment_repository import (
    SQLAlchemyCommentRepository,
)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()
router = APIRouter()


@router.get("/post/{post_id}", response_model=List[CommentOutput])
async def get_comments_by_post(
    post_id: str, comment_repo: CommentRepository = Depends(get_comment_repository)
):
    usecase = GetCommentsByPostUseCase(comment_repo)
    comments = usecase.execute(post_id)
    return comments


@router.get("/user", response_model=List[CommentOutput])
async def get_comments_by_user(
    comment_repo: CommentRepository = Depends(get_comment_repository),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user: User = Depends(get_current_user),
):
    usecase = GetCommentsByUserUseCase(comment_repo)
    comments = usecase.execute(user.id)
    return comments


@router.post("/", response_model=CommentOutput)
async def add_comment(
    data: AddCommentInput,
    comment_repo: CommentRepository = Depends(get_comment_repository),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user: User = Depends(get_current_user),
):
    if data.date.tzinfo is not None:
        data.date = data.date.replace(tzinfo=None)
    comment = Comment(
        id=str(uuid.uuid4()),
        post_id=data.post_id,
        user_id=user.id,
        comment=data.comment,
        date=data.date,
    )
    usecase = AddCommentUseCase(comment_repo)
    added_comment = usecase.execute(comment)
    return added_comment


@router.delete("/{comment_id}")
def delete_comment(
    comment_id: str, comment_repo: CommentRepository = Depends(get_comment_repository)
):
    usecase = DeleteCommentUseCase(comment_repo)
    success = usecase.execute(comment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Comment not found")
    return {"message": "Comment deleted successfully"}
