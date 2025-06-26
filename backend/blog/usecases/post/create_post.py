from blog.domain.entities.post import Post
from blog.domain.repositories.post_repository import PostRepository
from typing import Optional


class CreatePostUseCase:
    def __init__(self, repository: PostRepository):
        self.repository = repository

    def execute(self, post: Post) -> Optional[Post]:
        return self.repository.create(post)
