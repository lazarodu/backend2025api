from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from blog.domain.entities.comment import Comment
from blog.domain.repositories.comment_repository import CommentRepository
from blog.infra.models.comment_model import CommentModel


class SQLAlchemyCommentRepository(CommentRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_comments_by_post(self, post_id: str) -> List[Comment]:
        result = await self.session.execute(
            select(CommentModel).where(CommentModel.post_id == post_id)
        )
        return [c.to_entity() for c in result.scalars().all()]

    async def get_comments_by_user(self, user_id: str) -> List[Comment]:
        result = await self.session.execute(
            select(CommentModel).where(CommentModel.user_id == user_id)
        )
        return [c.to_entity() for c in result.scalars().all()]

    async def add_comment(self, comment: Comment) -> Comment:
        db_comment = CommentModel.from_entity(comment)
        self.session.add(db_comment)
        await self.session.commit()
        await self.session.refresh(db_comment)
        return db_comment.to_entity()

    async def delete_comment(self, comment_id: str) -> None:
        await self.session.execute(
            delete(CommentModel).where(CommentModel.id == comment_id)
        )
        await self.session.commit()
