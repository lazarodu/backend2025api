from blog.domain.repositories.comment_repository import CommentRepository
from blog.domain.entities.comment import Comment
from typing import List


class GetCommentsByUserUseCase:
    def __init__(self, repository: CommentRepository):
        self.repository = repository

    async def execute(self, user_id: str) -> List[Comment]:
        return await self.repository.get_comments_by_user(user_id)
