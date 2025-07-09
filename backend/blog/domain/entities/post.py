from datetime import datetime
from blog.domain.entities.user import User
from blog.domain.entities.comment import Comment
from typing import Optional, List


class Post:
    def __init__(
        self,
        id: str,
        title: str,
        description: str,
        content: str,
        user_id: str,
        date: datetime,
        user: Optional[User] = None,
        comments: Optional[List[Comment]] = None,
    ):
        self.id = id
        self.title = title
        self.description = description
        self.content = content
        self.user_id = user_id
        self.date = date
        self.user = user
        self.comments = comments or []
