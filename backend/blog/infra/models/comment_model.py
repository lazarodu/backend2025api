from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from blog.infra.database import Base
from datetime import datetime

class CommentModel(Base):
    __tablename__ = "comments"

    id = Column(String, primary_key=True, index=True)
    post_id = Column(String, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    comment = Column(Text, nullable=False)
    date = Column(DateTime, default=datetime.now, nullable=False)
