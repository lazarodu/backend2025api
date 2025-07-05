from abc import ABC, abstractmethod
from blog.domain.entities.post import Post
from typing import Optional


class PostRepository(ABC):
    @abstractmethod
    async def get_all(self) -> list[Post]:
        pass

    @abstractmethod
    async def get_by_id(self, post_id: str) -> Optional[Post]: ...

    @abstractmethod
    async def create(self, post: Post) -> Optional[Post]: ...

    @abstractmethod
    async def update(self, post: Post) -> Optional[Post]: ...

    @abstractmethod
    async def delete(self, post_id: str) -> None:
        pass
